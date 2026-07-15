USER PROMPT:

- Review `alt_text_plus_project/AGENTS.md` for coding-directives.

- Review `alt_text_plus_project/PLAN__add_lmstudio.md` to understand what to implement.

- Implement the plan!

MAIN RESPONSE:

Implemented the LM Studio/OpenRouter model-server plan. The code now uses provider-neutral `GeneratedAltText` persistence, a new `model_server_helpers` client for OpenAI-compatible `/chat/completions`, updated sync and background processing, renamed script `scripts/process_alt_text_generation.py`, updated settings/docs/templates/admin/tests, and a migration for the model rename and new `model_server`/`base_url` fields. Verified with `uv run ./run_tests.py`, `uv run ./manage.py makemigrations --check --dry-run`, `uv run ruff check .`, and `uv run ./scripts/process_alt_text_generation.py --help`.

---

USER PROMPT:

Goal: to update the test you (codex) recently set up using promptfoo and the new test-images.

Context:

- the problem with that was that we want to send those images to our lm-studio instance with two different models loaded so we can compare their responses.

- review `alt_text_plus_project/explore_assessments/promptfoo/promptfooconfig.yaml` to see an original example config that hits lm studio to compare model-responses. Consider using this as a template.

- This is what you created recently: `alt_text_plus_project/explore_assessments/promptfoo/promptfooconfig.initial-images.yaml` -- it works, but doesn't access models.

- Note that you will have to update `alt_text_plus_project/explore_assessments/promptfoo/initial_images_cases.yaml` because it's using hardcoded values instead of responses from the models.

Tasks:

- edit `alt_text_plus_project/explore_assessments/promptfoo/promptfooconfig.initial-images.yaml` -- and anything else necessary -- to send the images to two models so we can compare them in promptfoo.

MAIN RESPONSE:

Updated the initial-image Promptfoo scenario to call two LM Studio models at temperature 0: the app's first configured model and the model named by `ALT_TEXT_EVAL_MODEL_A`. Removed the fixture output and hardcoded reference alt text from all 11 image cases, and updated the Promptfoo README with the setup and no-cache run command. Verified both YAML files, all image paths, the two-provider/11-case structure, and all 37 project tests. The Promptfoo CLI itself was not installed locally, so no live model calls were made.

---
