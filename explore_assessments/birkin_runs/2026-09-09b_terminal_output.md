% PROMPTFOO_PYTHON="$PWD/.venv/bin/python" npx promptfoo@latest eval --no-cache -c explore_assessments/promptfoo/promptfooconfig.curated-four-images.yaml
(node:61674) ExperimentalWarning: DecompressInterceptor is experimental and subject to change
(Use `node --trace-warnings ...` to show where the warning was created)
Cache is disabled.
Starting evaluation eval-ZlQ-2026-09-09T14:58:44
Running 8 test cases (up to 1 at a time)...
Evaluating [████████████████████████████████████████] 100% | 8/8 | comparison-model-temperature-0 "# Context " case_id=1985.1122

┌────────────────┬────────────────┬────────────────┬────────────────┬────────────────┬────────────────┬────────────────┐
│ case_id        │ image_filename │ image_path     │ mime_type      │ ideal_alt_text │ [primary-conf… │ [comparison-m… │
│                │                │                │                │                │ alt_text_app/… │ alt_text_app/… │
│                │                │                │                │                │ # Context      │ # Context      │
│                │                │                │                │                │ - A user has   │ - A user has   │
│                │                │                │                │                │ uploaded an    │ uploaded an    │
│                │                │                │                │                │ image to an    │ image to an    │
│                │                │                │                │                │ alt...         │ alt...         │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1977.7         │ 1977.7_web.jpg │ ../curated_im… │ image/jpeg     │ A silver cup   │ [PASS] Silver  │ [FAIL] A       │
│                │                │                │                │ is shaped like │ sculpture      │ silver         │
│                │                │                │                │ a man riding   │ depicts a      │ sculpture      │
│                │                │                │                │ down a river.  │ laughing       │ depicting a    │
│                │                │                │                │ The man has a  │ figure seated  │ small primate  │
│                │                │                │                │ naked torso    │ in a boat-like │ or monkey      │
│                │                │                │                │ and sits at    │ vessel,        │ sitting on     │
│                │                │                │                │ the lip of the │ surrounded by  │ tangled        │
│                │                │                │                │ cup, his head  │ swirling,      │ driftwood.     │
│                │                │                │                │ tilted back.   │ tree-root-like │                │
│                │                │                │                │ The waves      │ forms.         │                │
│                │                │                │                │ envelop each   │                │                │
│                │                │                │                │ side of the    │                │                │
│                │                │                │                │ cup and its    │                │                │
│                │                │                │                │ upturned tip.  │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1938.431       │ 1938.431_web.… │ ../curated_im… │ image/jpeg     │ A small gold   │ [FAIL] Golden, │ [FAIL] Golden  │
│                │                │                │                │ plaque depicts │ stylized mask  │ relief         │
│                │                │                │                │ a face with    │ with           │ sculpture of a │
│                │                │                │                │ fangs, framed  │ intricate,     │ stylized face  │
│                │                │                │                │ by many        │ symmetrical    │ or mask,       │
│                │                │                │                │ serpent heads. │ patterns,      │ featuring      │
│                │                │                │                │ The plaque is  │ featuring      │ deeply carved  │
│                │                │                │                │ flat with      │ swirling eyes, │ lines that     │
│                │                │                │                │ raised         │ a central      │ define the     │
│                │                │                │                │ designs.       │ mouth, and     │ eyes, nose,    │
│                │                │                │                │                │ leaf-like      │ and mouth.     │
│                │                │                │                │                │ protrusions at │                │
│                │                │                │                │                │ the top and    │                │
│                │                │                │                │                │ bottom.        │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1967.127       │ 1967.127_web.… │ ../curated_im… │ image/jpeg     │ A horizontally │ [FAIL] A       │ [FAIL] A       │
│                │                │                │                │ oriented       │ detailed       │ detailed       │
│                │                │                │                │ engraving      │ etching        │ drawing        │
│                │                │                │                │ depicts many   │ depicts a      │ depicting a    │
│                │                │                │                │ muscular nude  │ chaotic battle │ chaotic battle │
│                │                │                │                │ men violently  │ scene with     │ scene where    │
│                │                │                │                │ fighting, some │ numerous nude  │ multiple       │
│                │                │                │                │ with swords,   │ male figures   │ muscular male  │
│                │                │                │                │ daggers, and   │ wielding       │ figures fight  │
│                │                │                │                │ other various  │ swords, axes,  │ and grapple,   │
│                │                │                │                │ weapons. In    │ and bows       │ wielding       │
│                │                │                │                │ the            │ amidst dense,  │ swords,        │
│                │                │                │                │ background,    │ tangled        │ spears, and    │
│                │                │                │                │ there is       │ vegetation.    │ axes.          │
│                │                │                │                │ foliage.       │ One figure     │                │
│                │                │                │                │                │ holds a sign   │                │
│                │                │                │                │                │ reading "OPUS  │                │
│                │                │                │                │                │ ARTISIUS       │                │
│                │                │                │                │                │ FLORENTINUS."  │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1985.112       │ 1985.112_web.… │ ../curated_im… │ image/jpeg     │ A shiny round  │ [PASS] An      │ [FAIL] A dark, │
│                │                │                │                │ bronze bowl    │ ornate bronze  │ globular       │
│                │                │                │                │ features two   │ bowl with two  │ ceramic bowl   │
│                │                │                │                │ small handles. │ handles,       │ with handles   │
│                │                │                │                │ Across the     │ featuring      │ and intricate  │
│                │                │                │                │ surface of the │ intricate      │ relief         │
│                │                │                │                │ bowl are       │ engraved       │ patterns       │
│                │                │                │                │ silver inlay   │ patterns and   │ decorating its │
│                │                │                │                │ script and     │ inscriptions   │ exterior       │
│                │                │                │                │ depictions of  │ in Chinese     │ surface.       │
│                │                │                │                │ a child.       │ characters.    │                │
└────────────────┴────────────────┴────────────────┴────────────────┴────────────────┴────────────────┴────────────────┘
✓ Eval complete (ID: eval-ZlQ-2026-09-09T14:58:44)

» View results: promptfoo view
» Share with your team: https://promptfoo.app
» Feedback: https://promptfoo.dev/feedback

Total Tokens: 2,589
  Provider: 2,589 (1,192 prompt, 1,397 completion)

Results:
  ✓ 2 passed (25.00%)
  ✗ 6 failed (75.00%)
  0 errors (0%)
Duration: 58s (concurrency: 1)
