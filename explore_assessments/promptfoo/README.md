# Promptfoo Alt-Text Assessment Scaffold

This directory contains a first Promptfoo harness for comparing alt-text model outputs outside the Django webapp runtime.

## Files

- `promptfooconfig.yaml` defines the prompt, provider combinations, and test file.
- `provider.py` wraps the app's existing OpenAI-compatible model-server helper path without writing Django database records.
- `cases.yaml` defines the first synthetic image cases.
- `images/` contains small generated images for initial smoke testing.

## Run

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
