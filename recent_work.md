# 2026-November-18 -- Round-two alt-text evaluation

Work done...

- Applied the review edits in `explore_assessments/promptfoo/case_editing/curated_cases.round2.edits.json` to a copy of `explore_assessments/promptfoo/curated_cases.edited.yaml`. Saved the revised cases in `explore_assessments/promptfoo/curated_cases.round2.edited.yaml`.
- Verified all 49 case IDs and descriptions. The 38 revised assertion lists matched the review edits exactly, and the other 11 cases matched the original byte for byte.
- Ran all 40 repository tests successfully. Separately, confirmed the revised Plaque case accepts “A gold mask with fangs.”
- Identified the LM Studio builds used for comparison as Qwen3-VL-4B-Instruct (MLX 8-bit) and Gemma-4-E2B-it (MLX 4-bit).
- From `alt_text_plus_project/`, ran `PROMPTFOO_PYTHON="$PWD/.venv/bin/python" npx promptfoo@0.125.1 eval --no-cache -c explore_assessments/promptfoo/promptfooconfig.curated-edited-models.yaml --tests explore_assessments/promptfoo/curated_cases.round2.edited.yaml`.
- By default, Promptfoo saves model evaluation results in its local SQLite database at `~/.promptfoo/promptfoo.db`.
- From `alt_text_plus_project/`, exported the saved run with `npx promptfoo@0.125.1 export eval 'eval-BDP-2026-11-18T15:43:22' -o explore_assessments/birkin_runs/2026-11-18_curated-round2-results.json`.
- Verified all 98 results in the exported JSON. Each model evaluated 49 images and passed all assertions on 7 images.

---
