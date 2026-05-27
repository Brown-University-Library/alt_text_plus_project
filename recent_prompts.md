USER PROMPT:

- Review `alt_text_plus_project/AGENTS.md` for coding-directives.

- Review `alt_text_plus_project/PLAN__add_lmstudio.md` to understand what to implement.

- Implement the plan!

MAIN RESPONSE:

Implemented the LM Studio/OpenRouter model-server plan. The code now uses provider-neutral `GeneratedAltText` persistence, a new `model_server_helpers` client for OpenAI-compatible `/chat/completions`, updated sync and background processing, renamed script `scripts/process_alt_text_generation.py`, updated settings/docs/templates/admin/tests, and a migration for the model rename and new `model_server`/`base_url` fields. Verified with `uv run ./run_tests.py`, `uv run ./manage.py makemigrations --check --dry-run`, `uv run ruff check .`, and `uv run ./scripts/process_alt_text_generation.py --help`.

---
