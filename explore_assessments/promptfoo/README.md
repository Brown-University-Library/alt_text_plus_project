# Promptfoo Alt-Text Assessment Scaffold

This directory contains a first Promptfoo harness for comparing alt-text model outputs outside the Django webapp runtime.

## Files

- `promptfooconfig.yaml` defines the prompt, provider combinations, and test file.
- `promptfooconfig.initial-images.yaml` compares two LM Studio models against the first BDR image set.
- `promptfooconfig.curated-calibration.yaml` checks the curated assertions against the human-reviewed descriptions without calling a model server.
- `promptfooconfig.curated-models.yaml` compares the primary configured model with a model named by `ALT_TEXT_EVAL_MODEL_A` across all 50 curated images.
- `provider.py` wraps the app's existing OpenAI-compatible model-server helper path without writing Django database records.
- `cases.yaml` defines the first synthetic image cases.
- `initial_images_cases.yaml` defines the initial image paths, reference alt text, and assertions applied to both models.
- `curated_cases.yaml` keeps each curated image, human-reviewed description, and seeded required-content assertions together.
- `images/` contains small generated images for basic framework checks.

## Curated 50-Image Evaluation

Run these commands from the project root.

First, validate both configurations and their external test file:

```bash
npx promptfoo@latest validate -c explore_assessments/promptfoo/promptfooconfig.curated-calibration.yaml
npx promptfoo@latest validate -c explore_assessments/promptfoo/promptfooconfig.curated-models.yaml
```

Calibrate the deterministic assertions against the saved human-reviewed descriptions. This run reads the local images to verify every path but does not call a model server:

```bash
PROMPTFOO_PYTHON="$PWD/.venv/bin/python" npx promptfoo@latest eval --no-cache -c explore_assessments/promptfoo/promptfooconfig.curated-calibration.yaml
```

All 50 cases should pass calibration. Each case requires a few central, visible details and limits trimmed output to 200 Unicode characters. The `icontains-all` checks are deliberately readable starting points. They use case-insensitive substring matching, so review failures manually and revise a required phrase when a visually correct description uses a reasonable synonym.

To compare two models, configure the app's primary model as usual and set the exact provider/model identifier for the second model:

```bash
export ALT_TEXT_EVAL_MODEL_A="provider/model-name"
PROMPTFOO_PYTHON="$PWD/.venv/bin/python" npx promptfoo@latest eval --no-cache -c explore_assessments/promptfoo/promptfooconfig.curated-models.yaml
npx promptfoo@latest view
```

To compare more models in one result table, copy the comparison-provider block in `promptfooconfig.curated-models.yaml`, give it a distinct label and `model_env_var`, and export that environment variable before the run. Keep temperature at `0` for the first comparison pass; vary one setting at a time in later runs.

Recommended next steps after the first model run:

1. Inspect required-content failures for correct synonym use before treating them as model failures.
2. Add image-specific terms only when they are both visually important and reliably identifiable from the image alone.
3. Review responses that pass the deterministic checks for hallucinated details, reading order, and unnecessary wording; these qualities need human judgment or a separately calibrated rubric.
4. Save stable model and parameter combinations as additional provider blocks so later runs remain comparable.

## Run

Configure LM Studio in the project `.env` with the first model as the first entry in `LMSTUDIO_MODEL_ORDER`. Load that model and the comparison model in LM Studio, then set the comparison model's exact LM Studio identifier in the shell:

```bash
export ALT_TEXT_EVAL_MODEL_A="comparison-model-id"
```

Run the comparison from the project root. `--no-cache` ensures that every image is sent to both models instead of reusing earlier Promptfoo results:

```bash
PROMPTFOO_PYTHON="$PWD/.venv/bin/python" npx promptfoo@latest eval --no-cache -c explore_assessments/promptfoo/promptfooconfig.initial-images.yaml
```

Then view the two model-response columns side by side:

```bash
npx promptfoo@latest view
```

Both providers use temperature `0`. The primary provider uses the first model in the app's configured model order. The comparison provider requires `ALT_TEXT_EVAL_MODEL_A`; it does not fall back to the primary model when that variable is absent.

The initial-image comparison runs one request at a time, with a one-second delay between requests. A provider call retries connection failures and temporary HTTP responses up to 10 total attempts, waiting 10 seconds between attempts. The 120-second request timeout applies separately to each attempt; a refused connection can still fail immediately and move to the next retry.

Each model response is checked with:

- `word-count`, requiring 10 to 200 words.
- `gleu`, comparing the response to the reference alt text with a `0.6` threshold.

## Model-Server Comparison

From the project root:

```bash
PROMPTFOO_PYTHON="$PWD/.venv/bin/python" npx promptfoo@latest eval -c explore_assessments/promptfoo/promptfooconfig.yaml
```

Then view results:

```bash
npx promptfoo@latest view
```

Promptfoo will use the same model-server environment variables as the webapp, including `MODEL_SERVER`, `OPENROUTER_API_KEY`, `OPENROUTER_MODEL_ORDER`, `LMSTUDIO_BASE_URL`, `LMSTUDIO_MODEL_ORDER`, and related settings.

To compare a specific second model without editing app settings, set:

```bash
ALT_TEXT_EVAL_MODEL_A="provider/model-name"
```

If `ALT_TEXT_EVAL_MODEL_A` is not set, the scaffold falls back to the app's first configured model so the evaluation remains runnable with existing app configuration.

## Current Scope

The initial-image assertions provide basic automated signals, while the Promptfoo response matrix supports side-by-side review. GLEU measures text overlap with the saved reference and should not be treated as a complete assessment of alt-text quality.
