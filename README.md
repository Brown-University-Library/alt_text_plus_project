[![CI tests](https://github.com/birkin/alt_text_project/actions/workflows/ci_tests.yaml/badge.svg)](https://github.com/birkin/alt_text_project/actions/workflows/ci_tests.yaml)



NOTE: _experimental_ to explore LLM-as-a-judge functionality.

More information will be addded here, but for now, see the [info.md file](alt_text_app/lib/info.md).

## Model server

The app can generate alt text through OpenRouter or a local LM Studio OpenAI-compatible server.

OpenRouter:

```env
MODEL_SERVER="openrouter"
OPENROUTER_API_KEY="..."
OPENROUTER_MODEL_ORDER="..."
```

LM Studio:

```env
MODEL_SERVER="lmstudio"
LMSTUDIO_BASE_URL="http://127.0.0.1:1234/v1"
LMSTUDIO_MODEL_ORDER="the-loaded-model-id"
LMSTUDIO_API_KEY="lm-studio"
```

For LM Studio, start the local server and load a vision-capable model before uploading images.

---
