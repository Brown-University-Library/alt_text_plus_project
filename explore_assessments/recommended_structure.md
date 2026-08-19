# Recommended Promptfoo Structure for Curated Images and Alt Text

## Recommendation

Keep the 50 images in `curated_images/` and extract the published alt text from
`good_alt_text.md` into a structured Promptfoo test-case file. Do not copy the
images or embed them as base64 data in the test data.

The Markdown contains 50 numbered entries, 50 alt-text blocks, and local links
that match the 50 filenames in `curated_images/`.

The preferred layout is a YAML test-case file. It keeps each image, its ideal
alt text, and its image-specific criteria together while allowing the same
criteria to run against either the human-reviewed text or model output.

## Option 1: Structured YAML Test Cases

Create `promptfoo/curated_cases.yaml` with one record per image:

```yaml
- description: Brush Washer
  vars:
    case_id: "1957.40"
    image_filename: 1957.40_web.jpg
    image_path: ../curated_images/1957.40_web.jpg
    mime_type: image/jpeg
    ideal_alt_text: >-
      A wide squat light blue glazed porcelaneous stoneware bowl
      features a cracked pattern in the glaze.
  assert:
    - type: icontains-all
      value:
        - bowl
        - light blue
        - glazed
      metric: required-content

    - type: javascript
      value: Array.from(output).length <= 200
      metric: maximum-200-characters
```

Use a calibration configuration whose provider returns `ideal_alt_text` as if
it were model output:

```yaml
providers:
  - id: file://provider.py
    label: human-reviewed-calibration-output
    config:
      output_var: ideal_alt_text
      require_image_path_exists: true

tests:
  - file://curated_cases.yaml
```

The existing `promptfoo/provider.py` supports both `output_var` and
`require_image_path_exists`, so this does not require a new provider.

This arrangement supports two stages:

1. Run the assertions against the human-reviewed alt text. A failure indicates
   that the criterion or its expected terms need to be reconsidered.
2. Use a model provider without `output_var` and run the same test cases and
   assertions against model responses.

Advantages:

- The image, human-reviewed output, and criteria remain visibly associated.
- Assertions can use structured lists, names, thresholds, and weights.
- Changes are readable in Git.
- Criteria can grow without CSV quoting and escaping becoming difficult.
- The ideal alt text remains available as a variable for later comparison
  criteria, even when the evaluated output comes from a model.

`icontains-all` performs case-insensitive substring checks. If a criterion
requires whole words rather than substrings, use regular expressions or a
small custom assertion instead.

Also note that Promptfoo's `word-count` assertion counts words. If the desired
limit is 200 characters, use a JavaScript or Python assertion that measures
characters rather than `word-count` with a maximum of 200.

## Option 2: Flat CSV Test Data

Create `promptfoo/curated_cases.csv` with ordinary columns for variables and
`__expected` columns for Promptfoo assertions:

```csv
case_id,image_filename,image_path,mime_type,ideal_alt_text,__expected1,__expected2
1957.40,1957.40_web.jpg,../curated_images/1957.40_web.jpg,image/jpeg,"A wide squat light blue glazed porcelaneous stoneware bowl features a cracked pattern in the glaze.","icontains-all:bowl,light blue,glazed","javascript:Array.from(output).length <= 200"
```

The calibration configuration can use the same provider settings as the YAML
option, with `output_var: ideal_alt_text`.

Advantages:

- The data can be reviewed or maintained in spreadsheet software.
- One row represents one image.
- Promptfoo converts ordinary columns into variables and `__expected`,
  `__expected1`, and similar columns into assertions.

Disadvantages:

- Commas and quotation marks in alt text or assertions require CSV escaping.
- Lists and more involved criteria are harder to read.
- Named metrics, thresholds, weights, and grouped assertions are less natural
  than in YAML.

## Final Choice

Use the structured YAML option. Keep `good_alt_text.md` as the research and
provenance document, make `promptfoo/curated_cases.yaml` the executable
Promptfoo data, and retain the image files in `curated_images/`.

## Promptfoo Documentation

- [Test-case configuration and external files](https://www.promptfoo.dev/docs/configuration/test-cases/)
- [Deterministic assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/deterministic/)
- [Python providers](https://www.promptfoo.dev/docs/providers/python/)
