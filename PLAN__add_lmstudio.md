# Plan: Add LM Studio as an Alternate Model Server

## Goal

Add support for choosing either OpenRouter or a locally running LM Studio server for image alt-text generation, while keeping the current OpenRouter workflow working.

The preferred approach is to use the OpenAI-compatible `/chat/completions` API shape for both providers. OpenRouter already uses that shape, and LM Studio supports an OpenAI-compatible local server.

## Current Code Review Summary

The existing implementation is functionally OpenRouter-specific in naming, settings, persistence, scripts, tests, and templates.

Primary integration path:

- `alt_text_app/views.py`
  - Uploads the image.
  - Saves the file and thumbnail.
  - Calls `sync_processing_helpers.attempt_synchronous_processing()`.
  - Reads generated alt text through `doc.openrouter_alt_text`.

- `alt_text_app/lib/sync_processing_helpers.py`
  - Sets `ImageDocument.processing_status`.
  - Creates/updates an `OpenRouterAltText` record.
  - Calls `openrouter_helpers`.
  - Handles timeout fallback by marking work as `pending`.

- `alt_text_app/lib/openrouter_helpers.py`
  - Loads the prompt.
  - Reads OpenRouter settings.
  - Builds OpenAI-compatible chat completion payload with text plus `image_url`.
  - Posts to `https://openrouter.ai/api/v1/chat/completions`.
  - Parses the response.
  - Persists the response to `OpenRouterAltText`.

- `scripts/process_openrouter_summaries.py`
  - Cron/background processor for pending work.
  - Reuses `openrouter_helpers`.
  - Assumes OpenRouter credentials and model order.

- `alt_text_app/models.py`
  - `OpenRouterAltText` is the persistence model.
  - The reverse relation is `ImageDocument.openrouter_alt_text`.
  - Several fields are provider-specific in name: `openrouter_response_id`, `openrouter_created_at`.

- `config/settings.py` and `config/settings_ci_tests.py`
  - Define `OPENROUTER_API_KEY`, `OPENROUTER_MODEL_ORDER`, and OpenRouter-specific timeout names.

- Templates/admin/tests/docs also contain OpenRouter-specific labels and references.

## Recommended Design

Introduce a provider-neutral LLM alt-text integration layer and migrate persistence names away from OpenRouter.

Recommended provider setting:

```env
MODEL_SERVER="openrouter"
```

Allowed values:

- `openrouter`
- `lmstudio`

Recommended additional settings:

```env
MODEL_SERVER="openrouter"

OPENROUTER_API_KEY=""
OPENROUTER_MODEL_ORDER="openrouter/model-one,openrouter/model-two"
OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"

LMSTUDIO_BASE_URL="http://127.0.0.1:1234/v1"
LMSTUDIO_API_KEY="lm-studio"
LMSTUDIO_MODEL_ORDER="local-model-name"

MODEL_SYNC_TIMEOUT_SECONDS="30"
MODEL_CRON_TIMEOUT_SECONDS="60"
```

Notes:

- Keep `OPENROUTER_API_KEY` and `OPENROUTER_MODEL_ORDER` so existing `.env` files continue to work.
- Add `OPENROUTER_BASE_URL` for symmetry and testability, defaulting to `https://openrouter.ai/api/v1`.
- Use `LMSTUDIO_API_KEY` even if LM Studio does not require a real key, because OpenAI-compatible client/server patterns often expect an Authorization header. Default can be `lm-studio` or blank depending on observed LM Studio behavior.
- Use provider-specific model order settings rather than one global model list, because OpenRouter model IDs and local LM Studio model IDs will differ.

## Proposed File-Level Changes

### 1. Settings

Update:

- `config/settings.py`
- `config/settings_ci_tests.py`
- `config/dotenv_example_file.txt`

Add:

- `MODEL_SERVER`
- `OPENROUTER_BASE_URL`
- `LMSTUDIO_BASE_URL`
- `LMSTUDIO_API_KEY`
- `LMSTUDIO_MODEL_ORDER`
- `MODEL_SYNC_TIMEOUT_SECONDS`
- `MODEL_CRON_TIMEOUT_SECONDS`

Keep existing timeout names temporarily or map them to the new names for compatibility:

```python
MODEL_SYNC_TIMEOUT_SECONDS = float(os.environ.get('MODEL_SYNC_TIMEOUT_SECONDS', OPENROUTER_SYNC_TIMEOUT_SECONDS))
MODEL_CRON_TIMEOUT_SECONDS = float(os.environ.get('MODEL_CRON_TIMEOUT_SECONDS', OPENROUTER_CRON_TIMEOUT_SECONDS))
```

During cleanup, replace internal usage with the provider-neutral timeout names.

### 2. Rename Persistence Model

Rename:

- `OpenRouterAltText` -> `GeneratedAltText` or `ModelAltText`
- `related_name='openrouter_alt_text'` -> `related_name='generated_alt_text'`

Recommended model name: `GeneratedAltText`.

Rename fields:

- `openrouter_response_id` -> `response_id`
- `openrouter_created_at` -> `response_created_at`

Add fields:

- `model_server = models.CharField(max_length=32, blank=True)`
- optionally `base_url = models.CharField(max_length=255, blank=True)` if it is useful for debugging local vs remote calls

FEEDBACK: yes, add that `base_url` field.

Keep fields:

- `provider`
- `model`
- `finish_reason`
- `raw_response_json`
- token fields
- `cost`

Migration approach:

- Use `migrations.RenameModel` from `OpenRouterAltText` to `GeneratedAltText`.
- Use `migrations.RenameField` for provider-specific fields.
- Use `migrations.AlterField` to change `related_name`.
- Use `migrations.AddField` for `model_server`.
- Update verbose names to provider-neutral labels.

### 3. Replace `openrouter_helpers.py` With Provider-Neutral Client Module

Create or rename to:

- `alt_text_app/lib/model_server_helpers.py`

Responsibilities:

- Load prompt.
- Read selected provider config.
- Build OpenAI-compatible chat completion payload.
- Add headers appropriate to the selected provider.
- Call `/chat/completions` for the selected provider.
- Try configured models in order.
- Parse a broadly OpenAI-compatible response.
- Persist to `GeneratedAltText`.

Suggested structures:

```python
class ModelServerConfig:
    server: str
    base_url: str
    api_key: str
    model_order: list[str]
    extra_headers: dict[str, str]
```

OpenRouter config should add:

- `HTTP-Referer: https://library.brown.edu`
- `X-Title: Image Alt Text Maker`

LM Studio config should probably only include:

- `Authorization: Bearer {api_key}` if `LMSTUDIO_API_KEY` is set
- `Content-Type: application/json`

The final URL should be:

```python
f'{base_url.rstrip("/")}/chat/completions'
```

### 4. Update Sync Processing

Update:

- `alt_text_app/lib/sync_processing_helpers.py`

Rename functions:

- `attempt_openrouter_sync()` -> `attempt_model_server_sync()` or `attempt_alt_text_sync()`

Change behavior:

- Read selected provider through the provider-neutral helper.
- Create/update `GeneratedAltText`.
- Use `MODEL_SYNC_TIMEOUT_SECONDS`.
- Keep timeout fallback behavior the same.
- Improve log messages to include `model_server` instead of assuming OpenRouter.

### 5. Update Background Script

Recommended rename:

- `scripts/process_openrouter_summaries.py` -> `scripts/process_alt_text_generation.py`

Update behavior:

- Use `GeneratedAltText`.
- Use `generated_alt_text` relation.
- Use provider-neutral helper.
- Validate settings for the selected `MODEL_SERVER`.
- Use `MODEL_CRON_TIMEOUT_SECONDS`.
- Log the selected model server and model order.

Compatibility option:

- Leave a thin wrapper script at `scripts/process_openrouter_summaries.py` that imports and calls the new script's `main()` so existing cron entries do not break immediately.

### 6. Update Views, Templates, Admin, and Docs

Update:

- `alt_text_app/views.py`
- `alt_text_app/admin.py`
- `alt_text_app/alt_text_app_templates/alt_text_app/report.html`
- `alt_text_app/alt_text_app_templates/alt_text_app/fragments/alt_text_fragment.html`
- `alt_text_app/lib/info.md`
- `README.md` if desired

Changes:

- Import `GeneratedAltText`.
- Read `doc.generated_alt_text`.
- Replace user-facing "OpenRouter" labels with provider-neutral language where appropriate.
- For metadata display, continue showing `model`; optionally show `model_server` in admin only.
- Update privacy text to distinguish remote OpenRouter from local LM Studio.

### 7. Update Tests

Update existing tests:

- `alt_text_app/tests/test_sync_processing.py`
- `alt_text_app/tests/test_polling_endpoints.py`
- `alt_text_app/tests/test_upload_view.py` if patch paths change

Add focused tests for:

- `MODEL_SERVER=openrouter` builds OpenRouter URL, auth header, OpenRouter extra headers, and model order.
- `MODEL_SERVER=lmstudio` builds local LM Studio URL and uses LM Studio model order.
- Missing settings fail clearly for the selected provider.
- Response parsing works for a standard OpenAI-compatible response.
- Timeout fallback still marks generated alt text as `pending`.
- Background processor finds records through `generated_alt_text`.

### 8. Documentation and Local Usage

Document LM Studio setup in `README.md` or `alt_text_app/lib/info.md`:

1. Start LM Studio.
2. Load a vision-capable model.
3. Start the local OpenAI-compatible server.
4. Set:

```env
MODEL_SERVER="lmstudio"
LMSTUDIO_BASE_URL="http://127.0.0.1:1234/v1"
LMSTUDIO_MODEL_ORDER="the-loaded-model-id"
LMSTUDIO_API_KEY="lm-studio"
```

Also document switching back:

```env
MODEL_SERVER="openrouter"
OPENROUTER_API_KEY="..."
OPENROUTER_MODEL_ORDER="..."
```

## Implementation Sequence

1. Add settings and `.env` example entries.
2. Rename the persistence model and fields in `models.py`.
3. Generate and inspect the Django migration.
4. Add `model_server_helpers.py` with provider config, request building, response parsing, and persistence.
5. Update sync processing to use `GeneratedAltText` and `model_server_helpers`.
6. Rename/update the background script and optionally keep the old script as a wrapper.
7. Update views, templates, admin, and docs.
8. Update tests and patch import paths.
9. Run:

```bash
uv run ./run_tests.py
```

10. Manually test both modes:

```env
MODEL_SERVER="openrouter"
```

and:

```env
MODEL_SERVER="lmstudio"
```

## Open Decision Points

### Decision 1: Model Class Name

Recommendation: `GeneratedAltText`.

FEEDBACK: GeneratedAltText is fine.

Alternatives:

- `ModelAltText`
- `LLMAltText`
- `AltTextGeneration`

`GeneratedAltText` reads clearly in admin and does not expose implementation jargon.

### Decision 2: Script Rename Compatibility

Recommendation: create `scripts/process_alt_text_generation.py` and leave `scripts/process_openrouter_summaries.py` as a wrapper for one release/deployment cycle.

FEEDBACK: No, don't leave the old script as a wrapper. Just rename it.

Open question: are there existing cron entries or deployment docs that directly call `process_openrouter_summaries.py`?

FEEDBACK: No

### Decision 3: LM Studio Authorization Header

Recommendation: support `LMSTUDIO_API_KEY`, but omit the Authorization header if it is blank.

Open question: should the default `.env` example set `LMSTUDIO_API_KEY="lm-studio"` or leave it blank?

FEEDBACK: use `LMSTUDIO_API_KEY="lm-studio"`

### Decision 4: Provider-Specific Model Order vs Shared Model Setting

Recommendation: use provider-specific model order settings:

- `OPENROUTER_MODEL_ORDER`
- `LMSTUDIO_MODEL_ORDER`

Open question: should LM Studio support a model order list, or just a single `LMSTUDIO_MODEL`? A list keeps the implementation symmetrical, but local fallback may be less useful.

FEEDBACK: have it support a model order list for now. Add a TO-DO-IN-FUTURE section add a note to review the whole order concept.

### Decision 5: Storing `base_url`

Recommendation: store `model_server` on each generated alt-text row, but do not store `base_url` unless debugging requires it.

FEEDBACK: store the `base_url` too.

Open question: would recording local endpoint details in the database be helpful for experiment reproducibility, or undesirable because local URLs are environment-specific?

### Decision 6: OpenRouter Legacy Setting Names

Recommendation: keep current OpenRouter setting names in `.env` and code settings. Generalize internal helper names, not every provider-specific env var.

Open question: should there also be fully generic aliases like `MODEL_API_KEY` and `MODEL_MODEL_ORDER`, or is explicit provider config clearer?

FEEDBACK: you already suggested specific separate model-specific settings, which i like, so keep that approach.

### Decision 7: Prompt Differences by Provider

Recommendation: use the current shared `prompt.md` for both providers at first.

FEEDBACK: keep the current shared `prompt.md` for now.

Open question: should LM Studio get its own prompt file if local model behavior differs significantly?

### Decision 8: LM Studio Vision Payload Compatibility

Recommendation: start with the same OpenAI-compatible `image_url` data URL payload:

```json
{
  "type": "image_url",
  "image_url": {
    "url": "data:image/png;base64,..."
  }
}
```

FEEDBACK: yes, start with the same OpenAI-compatible `image_url` data URL payload.

Open question: confirm that the target LM Studio version and loaded model support this exact multimodal payload. If not, add a provider-specific payload builder while keeping the higher-level interface shared.

## Original Prompt

```text
Goal: Make a plan to add the ability to _either_ use open-router or a locally-running LM-Studio.

Context:

- The current working code uses OpenRouter to submit an image for alt-text.

- I want this to continue to work.

- I _also_ want to be able to use LM-Studio, running locally, to experiment with.

- Feel free to suggest approaches -- but I'm thinking I could add a `.env` setting, something like, "MODEL_SERVER", with the value either of "openrouter" or "lmstudio".

- I think LM-Studio has it's own rest-api-url pattern -- but I think OpenRouter is using the OpenAI-rest-api-url pattern -- so let's use that OpenAI-rest-api-url pattern because I believe LM-Studio supports it.

Tasks:

- Review all the `alt_text_plus_project` code.

- Create and save an implementation plan to `alt_text_plus_project/PLAN__add_lmstudio.md` 

- Clearly indicate open-decision-points.

- Append this prompt at the end of the plan.
```
