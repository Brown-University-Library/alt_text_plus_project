# AI Assessment Framework Recommendation

## Table of Contents

- [Context](#context)
- [Recommendation](#recommendation)
- [Evaluated Options](#evaluated-options)
- [Why Promptfoo First](#why-promptfoo-first)
- [Suggested First Implementation Shape](#suggested-first-implementation-shape)
- [When To Add DeepEval](#when-to-add-deepeval)
- [Why Not Weights & Biases First](#why-not-weights--biases-first)
- [Sources](#sources)
- [Original Prompt](#original-prompt)

## Context

This project has a working Django webapp that generates alt text for uploaded images through OpenRouter or a local LM Studio OpenAI-compatible server. The next step is not to define quality criteria yet, but to choose a lightweight open-source framework for comparing models, prompts, and parameters outside the normal webapp request flow.

The assessment code should live in this repo, but should not become part of the production user-facing app path.

## Recommendation

Start with **Promptfoo**.

Promptfoo is the best fit for this project because it is lightweight, open-source, locally runnable, and designed around the first workflow this project needs: run the same cases across multiple providers, models, prompts, and parameters, then inspect results side-by-side. It can start without automated scoring, which matches the current scope. Automated checks or model-judge scoring can be added later.

Promptfoo also supports custom Python providers, which means an evaluation harness can call this project's existing model-server helper code instead of duplicating the OpenRouter/LM Studio request logic or adding framework-specific code to the Django request path.

## Evaluated Options

| Framework | Fit | Notes |
| --- | --- | --- |
| **Promptfoo** | **Best first choice** | Lightweight external harness; simple YAML configuration; local CLI and local web viewer; compares providers and parameters in a matrix; supports custom Python providers; suitable for manual review first and automated checks later. |
| **DeepEval** | Strong second choice | Python-native and pytest-like, which fits this Django/uv project well. Better if the team wants evaluation to look like test code. Strong for LLM-as-judge workflows and custom metrics, but many useful metrics require a judge model and it is more pass/fail oriented than Promptfoo. |
| **Ragas** | Useful later, not first | Open-source Python evaluation toolkit with useful metric primitives, but its strongest fit is RAG and testset-generation workflows. This project is currently image-to-alt-text generation, so Ragas is likely more framework than needed for the first assessment pass. |

## Why Promptfoo First

- It can live under a repo-local `explore_assessments/` or `evals/` directory without changing the webapp.
- It supports matrix-style comparison of models, prompts, and parameters.
- It can begin with human review of generated outputs rather than forcing premature scoring decisions.
- It has a local web viewer, which should help a small team inspect differences without building custom UI.
- It can use a Python provider wrapper around existing project code.
- It can later support assertions, grading, CI runs, and regression tracking if the workflow matures.

## Suggested First Implementation Shape

Create a small evaluation harness outside the app runtime:

```text
explore_assessments/
  framework_recommendation.md
  promptfoo/
    promptfooconfig.yaml
    provider.py
    cases.yaml
    images/
```

The first Promptfoo prototype should:

1. Use a small curated set of images.
2. Run the same prompt against two or three model/parameter combinations.
3. Capture generated alt text plus metadata such as model, provider, latency, token usage, and cost when available.
4. Use Promptfoo's local viewer for side-by-side review.
5. Avoid quality scoring until the team defines quality criteria.

## When To Add DeepEval

Add DeepEval later if the team wants:

- Python test files instead of YAML-first configuration.
- LLM-as-judge checks with custom criteria.
- CI-style pass/fail thresholds for a stable regression suite.
- Closer integration with Python unit-test patterns.

DeepEval should be treated as a second-phase tool, not the first exploration framework.

## Why Not Weights & Biases First

Weights & Biases/Weave is relevant and has open-source pieces, but it is heavier than this step requires. It is more of an experiment tracking and observability platform, and its quickstart expects a W&B account. That may be useful later if the project needs persistent experiment tracking, dashboards, or traces, but it is not the lightest first framework for a small repo-local exploration.

## Sources

- Promptfoo docs: <https://www.promptfoo.dev/docs/intro/>
- Promptfoo configuration docs: <https://www.promptfoo.dev/docs/configuration/guide/>
- Promptfoo Python provider docs: <https://www.promptfoo.dev/docs/providers/python/>
- Promptfoo CLI/view docs: <https://www.promptfoo.dev/docs/usage/command-line/>
- DeepEval docs: <https://deepeval.com/docs/getting-started>
- DeepEval GitHub: <https://github.com/confident-ai/deepeval>
- Ragas docs: <https://docs.ragas.io/en/latest/>
- Ragas GitHub: <https://github.com/vibrantlabsai/ragas>
- Weave GitHub: <https://github.com/wandb/weave>

## Original Prompt

```text
Goal: Pick an assessment framework.

Context:

- We have a working webapp that can generate alt-text.

- We want to figure out how to assess different models/parameters.

- We know there are "frameworks" for ai-assessment (we've heard of weights-and-biases, for example).

- We want to work with an open-source _lightweight_ framework, easy for a small team to implement and work with.

- Actually assessing quality is outside of the scope of this step -- this step is about picking a framework.

- We assume working with the assessment framework will be "outside" of the operation of this webapp -- but we'll keep any code in the repo-project.

Tasks:

- research and evaluate the top two or three lightweight open-source assessment frameworks that we can implement for this project and begin exploring.
```
