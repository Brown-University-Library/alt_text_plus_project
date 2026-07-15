# Promptfoo Alt-Text Assessment Scaffold

This directory contains a first Promptfoo harness for comparing alt-text model outputs outside the Django webapp runtime.

## Files

- `promptfooconfig.yaml` defines the prompt, provider combinations, and test file.
- `promptfooconfig.initial-images.yaml` compares two LM Studio models against the first BDR image set.
- `provider.py` wraps the app's existing OpenAI-compatible model-server helper path without writing Django database records.
- `cases.yaml` defines the first synthetic image cases.
- `initial_images_cases.yaml` defines the initial image paths sent to both models.
- `images/` contains small generated images for basic framework checks.

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

This scaffold intentionally does not grade output quality. The first pass is for side-by-side review of model and parameter behavior. Add assertions only after the team defines quality criteria for useful alt text.
