It seems like a promptfoo run should be saved somewhere where it can be committed, but I just ran:

```
% PROMPTFOO_PYTHON="$PWD/.venv/bin/python" npx promptfoo@latest eval --no-cache -c explore_assessments/promptfoo/promptfooconfig.curated-models.yaml 
```

...and git showed no new files to commit, so am pasting below.

```
% PROMPTFOO_PYTHON="$PWD/.venv/bin/python" npx promptfoo@latest eval --no-cache -c explore_assessments/promptfoo/promptfooconfig.curated-models.yaml 
(node:36061) ExperimentalWarning: DecompressInterceptor is experimental and subject to change
(Use `node --trace-warnings ...` to show where the warning was created)
Cache is disabled.
Starting evaluation eval-XIJ-2026-09-09T13:41:17
Running 100 test cases (up to 1 at a time)...
Evaluating [████████████████████████████████████████] 100% | 100/100 | comparison-model-temperature-0 "# Context " case_id=1958w

┌────────────────┬────────────────┬────────────────┬────────────────┬────────────────┬────────────────┬────────────────┐
│ case_id        │ image_filename │ image_path     │ mime_type      │ ideal_alt_text │ [primary-conf… │ [comparison-m… │
│                │                │                │                │                │ alt_text_app/… │ alt_text_app/… │
│                │                │                │                │                │ # Context      │ # Context      │
│                │                │                │                │                │ - A user has   │ - A user has   │
│                │                │                │                │                │ uploaded an    │ uploaded an    │
│                │                │                │                │                │ image to an    │ image to an    │
│                │                │                │                │                │ alt...         │ alt...         │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1977.7         │ 1977.7_web.jpg │ ../curated_im… │ image/jpeg     │ A silver cup   │ [FAIL] Silver  │ [FAIL] A       │
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
│                │                │                │                │ raised         │ a bearded      │ define the     │
│                │                │                │                │ designs.       │ face, and      │ eyes, nose,    │
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
│ 1926.533       │ 1926.533_web.… │ ../curated_im… │ image/jpeg     │ A large,       │ [FAIL] An      │ [FAIL] A       │
│                │                │                │                │ vertically     │ ornate,        │ richly         │
│                │                │                │                │ long carpet    │ rectangular    │ patterned rug  │
│                │                │                │                │ features       │ rug with a     │ featuring      │
│                │                │                │                │ elaborate      │ symmetrical    │ intricate      │
│                │                │                │                │ floral         │ floral and     │ floral and     │
│                │                │                │                │ patterns in    │ geometric      │ geometric      │
│                │                │                │                │ shades of      │ pattern in     │ motifs in      │
│                │                │                │                │ orange, blue,  │ shades of      │ earthy tones   │
│                │                │                │                │ green, and     │ orange, green, │ of orange,     │
│                │                │                │                │ brown. It is   │ blue, and      │ brown, green,  │
│                │                │                │                │ trimmed with   │ brown,         │ and muted      │
│                │                │                │                │ fringe on the  │ featuring      │ blue.          │
│                │                │                │                │ two shortest   │ fringe along   │                │
│                │                │                │                │ sides.         │ the bottom     │                │
│                │                │                │                │                │ edge.          │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 2007.193       │ 2007.193_web.… │ ../curated_im… │ image/jpeg     │ A small wood   │ [FAIL] Carved  │ [FAIL] A dark, │
│                │                │                │                │ figure with    │ wooden figure  │ reddish-brown  │
│                │                │                │                │ the face of a  │ with a fierce, │ wooden carving │
│                │                │                │                │ feline bares   │ stylized face, │ of a figure    │
│                │                │                │                │ its teeth. It  │ wearing a      │ wearing an     │
│                │                │                │                │ draws a knife  │ detailed       │ elaborate      │
│                │                │                │                │ across the     │ headdress and  │ headdress and  │
│                │                │                │                │ throat of a    │ seated in a    │ mask,          │
│                │                │                │                │ human in its   │ crouched       │ featuring      │
│                │                │                │                │ lap. The       │ position.      │ detailed       │
│                │                │                │                │ entire surface │                │ facial         │
│                │                │                │                │ of the figure  │                │ features and   │
│                │                │                │                │ has been       │                │ stylized       │
│                │                │                │                │ carved with    │                │ clothing.      │
│                │                │                │                │ geometric      │                │                │
│                │                │                │                │ patterns.      │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1925.1293      │ 1925.1293_web… │ ../curated_im… │ image/jpeg     │ A vertically   │ [FAIL] Carved  │ [FAIL] A       │
│                │                │                │                │ oriented       │ ivory panel    │ carved relief  │
│                │                │                │                │ carved ivory   │ depicting the  │ depicting the  │
│                │                │                │                │ relief depicts │ Virgin Mary    │ Madonna and    │
│                │                │                │                │ a woman seated │ seated with    │ Child, flanked │
│                │                │                │                │ in the center  │ the Christ     │ by angels, set │
│                │                │                │                │ holding a      │ Child, flanked │ within an      │
│                │                │                │                │ child in her   │ by angels, on  │ ornate frame.  │
│                │                │                │                │ lap. Two       │ an ornate      │ Greek text is  │
│                │                │                │                │ angels hover   │ throne with    │ visible at the │
│                │                │                │                │ above, one in  │ Greek          │ base of the    │
│                │                │                │                │ each upper     │ inscription    │ sculpture.     │
│                │                │                │                │ corner. There  │ below.         │                │
│                │                │                │                │ are letters    │                │                │
│                │                │                │                │ carved         │                │                │
│                │                │                │                │ beneath.       │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 2012.43        │ 2012.43_web.j… │ ../curated_im… │ image/jpeg     │ A tall         │ [FAIL] A tall, │ [FAIL] A tall, │
│                │                │                │                │ reddish-brown  │ polished       │ antique wooden │
│                │                │                │                │ wood bookcase  │ wooden         │ cabinet with   │
│                │                │                │                │ features many  │ secretary desk │ two doors and  │
│                │                │                │                │ drawers and    │ with a curved  │ a section of   │
│                │                │                │                │ components. It │ top and five   │ drawers,       │
│                │                │                │                │ is detailed    │ drawers, each  │ featuring      │
│                │                │                │                │ with simple    │ adorned with   │ ornate molding │
│                │                │                │                │ but refined    │ ornate brass   │ and brass      │
│                │                │                │                │ designs and    │ handles.       │ hardware.      │
│                │                │                │                │ shiny brass    │                │                │
│                │                │                │                │ knobs and      │                │                │
│                │                │                │                │ handles.       │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 2003.40        │ 2003.40_web.j… │ ../curated_im… │ image/jpeg     │ A realistic,   │ [FAIL] Bronze  │ [FAIL] Bronze  │
│                │                │                │                │ hand-painted   │ bust of a      │ sculpture      │
│                │                │                │                │ plaster        │ young boy      │ portrait of a  │
│                │                │                │                │ sculpture      │ wearing a cap  │ person with    │
│                │                │                │                │ depicts a      │ and collared   │ dark skin      │
│                │                │                │                │ Black boy's    │ shirt, with    │ wearing a cap  │
│                │                │                │                │ head and top   │ the name       │ and collared   │
│                │                │                │                │ half of his    │ "GAMAL"        │ shirt.         │
│                │                │                │                │ torso. The     │ inscribed on   │                │
│                │                │                │                │ sculpture      │ the base.      │                │
│                │                │                │                │ looks like     │                │                │
│                │                │                │                │ bronze and the │                │                │
│                │                │                │                │ subject wears  │                │                │
│                │                │                │                │ a flat cap and │                │                │
│                │                │                │                │ looks slightly │                │                │
│                │                │                │                │ to our left.   │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1953.386       │ 1953.386_web.… │ ../curated_im… │ image/jpeg     │ A ladle        │ [FAIL] An      │ [FAIL]         │
│                │                │                │                │ features a     │ ornate ladle   │ Handcrafted    │
│                │                │                │                │ large light    │ with a long    │ artifact       │
│                │                │                │                │ brown spoon    │ handle         │ featuring a    │
│                │                │                │                │ and a long     │ featuring a    │ long, curved   │
│                │                │                │                │ dark brown     │ bird-headed    │ handle and an  │
│                │                │                │                │ handle. The    │ finial and     │ elongated      │
│                │                │                │                │ top of the     │ decorative     │ bowl-like end  │
│                │                │                │                │ ladle's handle │ inlaid         │ shaped like a  │
│                │                │                │                │ is an eagle    │ patterns. The  │ bird's head.   │
│                │                │                │                │ head. The      │ bowl is curved │                │
│                │                │                │                │ bottom of the  │ and shows      │                │
│                │                │                │                │ spoon has been │ signs of age   │                │
│                │                │                │                │ carved to      │ and use.       │                │
│                │                │                │                │ resemble a     │                │                │
│                │                │                │                │ bear's face.   │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1961.31        │ 1961.31_web.j… │ ../curated_im… │ image/jpeg     │ A small light  │ [FAIL]         │ [FAIL]         │
│                │                │                │                │ green segment  │ Fragmented     │ Sculpted head  │
│                │                │                │                │ of a head      │ stone head     │ or bust with   │
│                │                │                │                │ features the   │ sculpture with │ stylized       │
│                │                │                │                │ face of a      │ serene facial  │ features,      │
│                │                │                │                │ figure from    │ features,      │ including a    │
│                │                │                │                │ below the eyes │ showing signs  │ prominent nose │
│                │                │                │                │ to the top of  │ of age         │ and defined    │
│                │                │                │                │ the neck.      │ including      │ facial         │
│                │                │                │                │ There is a     │ cracks and     │ structure.     │
│                │                │                │                │ hole in each   │ discoloration. │                │
│                │                │                │                │ earlobe and    │                │                │
│                │                │                │                │ the figure's   │                │                │
│                │                │                │                │ mouth is       │                │                │
│                │                │                │                │ slightly open. │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1989.3         │ 1989.3_web.jpg │ ../curated_im… │ image/jpeg     │ A bronze bell  │ [FAIL] An      │ [FAIL]         │
│                │                │                │                │ features a     │ ancient bronze │ Weathered      │
│                │                │                │                │ green surface, │ bell with a    │ bronze plaque  │
│                │                │                │                │ engraved with  │ tall handle,   │ with raised    │
│                │                │                │                │ designs and    │ featuring      │ bosses and     │
│                │                │                │                │ inscriptions.  │ intricate      │ decorative     │
│                │                │                │                │ Three rows of  │ engraved       │ scrollwork,    │
│                │                │                │                │ six small      │ patterns and   │ mounted on a   │
│                │                │                │                │ knobs protrude │ small          │ cylindrical    │
│                │                │                │                │ from each side │ protruding     │ shaft.         │
│                │                │                │                │ of the bell.   │ knobs along    │                │
│                │                │                │                │                │ its surface.   │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1965.470       │ 1965.470_web.… │ ../curated_im… │ image/jpeg     │ A vertically   │ [FAIL] A       │ [FAIL] A       │
│                │                │                │                │ oriented       │ detailed       │ graphite       │
│                │                │                │                │ drawing with   │ sketch of a    │ drawing        │
│                │                │                │                │ gray tones of  │ human arm and  │ depicting a    │
│                │                │                │                │ an arm, bent   │ hand holding a │ human forearm  │
│                │                │                │                │ at the elbow,  │ sphere, dated  │ and hand       │
│                │                │                │                │ holds up a     │ 1507.          │ grasping a     │
│                │                │                │                │ spherical      │                │ spherical      │
│                │                │                │                │ object.        │                │ object.        │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 2002.45        │ 2002.45_web.j… │ ../curated_im… │ image/jpeg     │ A horizontally │ [FAIL] A       │ [FAIL] A wide, │
│                │                │                │                │ oriented       │ horse-drawn    │ arid landscape │
│                │                │                │                │ photograph     │ carriage       │ featuring sand │
│                │                │                │                │ depicts vast   │ travels across │ dunes leading  │
│                │                │                │                │ sand dunes     │ a vast desert  │ up to a large  │
│                │                │                │                │ with           │ landscape,     │ mountain. A    │
│                │                │                │                │ footprints. On │ with large     │ wagon with     │
│                │                │                │                │ our left, a    │ sand dunes     │ horses is      │
│                │                │                │                │ wagon in the   │ dominating the │ visible in the │
│                │                │                │                │ distance is    │ horizon under  │ middle ground  │
│                │                │                │                │ pulled by a    │ a pale sky.    │ against the    │
│                │                │                │                │ team of four   │                │ pale terrain.  │
│                │                │                │                │ horses.        │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1963.513       │ 1963.513_web.… │ ../curated_im… │ image/jpeg     │ A black box is │ [FAIL] A       │ [FAIL] A       │
│                │                │                │                │ painted with   │ rectangular,   │ small,         │
│                │                │                │                │ small, simple  │ dark brown box │ rectangular    │
│                │                │                │                │ clusters of    │ with gold      │ box with a     │
│                │                │                │                │ golden flowers │ floral         │ dark           │
│                │                │                │                │ all around.    │ patterns and a │ background     │
│                │                │                │                │ The knob of    │ gold ring      │ decorated with │
│                │                │                │                │ the box is in  │ handle.        │ gold floral    │
│                │                │                │                │ the shape of a │                │ patterns.      │
│                │                │                │                │ small gold     │                │                │
│                │                │                │                │ flower.        │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1958.21        │ 1958.21_web.j… │ ../curated_im… │ image/jpeg     │ A colorful oil │ [FAIL] A       │ [FAIL] A       │
│                │                │                │                │ painting       │ vibrant,       │ landscape      │
│                │                │                │                │ depicts a      │ impressionist… │ painting       │
│                │                │                │                │ landscape with │ landscape      │ depicting a    │
│                │                │                │                │ green trees    │ featuring      │ large mountain │
│                │                │                │                │ and a          │ rolling hills, │ peak under a   │
│                │                │                │                │ mountain, all  │ dense green    │ bright blue    │
│                │                │                │                │ under a blue   │ trees, and a   │ sky, with      │
│                │                │                │                │ sky.           │ bright blue    │ dense green    │
│                │                │                │                │                │ sky with       │ foliage and    │
│                │                │                │                │                │ swirling       │ reddish-brown  │
│                │                │                │                │                │ clouds. The    │ earth in the   │
│                │                │                │                │                │ foreground     │ foreground.    │
│                │                │                │                │                │ shows textured │                │
│                │                │                │                │                │ earth tones    │                │
│                │                │                │                │                │ and bold       │                │
│                │                │                │                │                │ brushstrokes.  │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1991.1         │ 1991.1_web.jpg │ ../curated_im… │ image/jpeg     │ A large black  │ [FAIL] Black   │ [FAIL] Ancient │
│                │                │                │                │ ceramic vessel │ Greek ceramic  │ pottery vessel │
│                │                │                │                │ features       │ vessel with    │ with dark      │
│                │                │                │                │ handles that   │ red and gold   │ glaze and      │
│                │                │                │                │ curve up.      │ painted scenes │ painted relief │
│                │                │                │                │ Around the     │ depicting      │ figures,       │
│                │                │                │                │ vessel are two │ mythological   │ featuring      │
│                │                │                │                │ scenes in      │ figures, a     │ animals in a   │
│                │                │                │                │ brown ceramic  │ sunburst, and  │ central        │
│                │                │                │                │ of tragedies   │ decorative     │ circular motif │
│                │                │                │                │ dealing with   │ borders.       │ surrounded by  │
│                │                │                │                │ children.      │                │ geometric      │
│                │                │                │                │                │                │ patterns.      │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1966.118       │ 1966.118_web.… │ ../curated_im… │ image/jpeg     │ A handscroll   │ [FAIL] A long  │ [FAIL] A       │
│                │                │                │                │ is filled with │ horizontal     │ series of      │
│                │                │                │                │ Japanese       │ scroll         │ vertical ink   │
│                │                │                │                │ calligraphy on │ depicting a    │ wash drawings  │
│                │                │                │                │ top of         │ series of ink  │ or calligraphy │
│                │                │                │                │ paintings of   │ wash           │ studies,       │
│                │                │                │                │ tall grass     │ landscapes     │ featuring      │
│                │                │                │                │ with lions     │ with sparse    │ sparse         │
│                │                │                │                │ leaping about. │ vegetation and │ brushstrokes   │
│                │                │                │                │                │ calligraphic   │ and            │
│                │                │                │                │                │ inscriptions.  │ handwritten    │
│                │                │                │                │                │                │ characters on  │
│                │                │                │                │                │                │ light paper.   │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 2009.271       │ 2009.271_web.… │ ../curated_im… │ image/jpeg     │ A marble       │ [FAIL] Marble  │ [FAIL] Marble  │
│                │                │                │                │ relief depicts │ relief         │ relief         │
│                │                │                │                │ the side       │ portrait of a  │ depicting a    │
│                │                │                │                │ profile of     │ man in         │ classical      │
│                │                │                │                │ Julius Caesar, │ profile,       │ profile        │
│                │                │                │                │ facing our     │ framed by an   │ portrait,      │
│                │                │                │                │ left,          │ ornate, curved │ framed by a    │
│                │                │                │                │ surrounded by  │ border adorned │ wreath of      │
│                │                │                │                │ a circular     │ with           │ foliage. Roman │
│                │                │                │                │ garland.       │ grapevines and │ numerals (IV)  │
│                │                │                │                │                │ leaves. The    │ and letters    │
│                │                │                │                │                │ inscription    │ (CE) are       │
│                │                │                │                │                │ "IV CE" is     │ inscribed      │
│                │                │                │                │                │ visible above  │ above the      │
│                │                │                │                │                │ the portrait.  │ subject's      │
│                │                │                │                │                │                │ head.          │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1985.112       │ 1985.112_web.… │ ../curated_im… │ image/jpeg     │ A shiny round  │ [FAIL] An      │ [FAIL] A dark, │
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
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1961.205       │ 1961.205_web.… │ ../curated_im… │ image/jpeg     │ A painted      │ [FAIL] Ancient │ [FAIL] Ancient │
│                │                │                │                │ limestone      │ Egyptian       │ stone relief   │
│                │                │                │                │ block features │ relief carving │ carving        │
│                │                │                │                │ three figures, │ depicting      │ depicting two  │
│                │                │                │                │ in profile     │ three figures  │ standing       │
│                │                │                │                │ facing our     │ in ceremonial  │ figures        │
│                │                │                │                │ right, each    │ attire,        │ flanked by     │
│                │                │                │                │ carrying a     │ surrounded by  │ vertical       │
│                │                │                │                │ tray of many   │ hieroglyphs    │ panels filled  │
│                │                │                │                │ objects and    │ and symbolic   │ with various   │
│                │                │                │                │ having an      │ offerings like │ plants,        │
│                │                │                │                │ animal by      │ animals, food, │ fruits, and    │
│                │                │                │                │ their side.    │ and ritual     │ vessels.       │
│                │                │                │                │ The figures    │ objects.       │                │
│                │                │                │                │ are separated  │                │                │
│                │                │                │                │ by many        │                │                │
│                │                │                │                │ hieroglyphics. │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 2004.87        │ 2004.87_web.j… │ ../curated_im… │ image/jpeg     │ A vertically   │ [FAIL] A       │ [FAIL]         │
│                │                │                │                │ oriented print │ monochromatic  │ Monochrome     │
│                │                │                │                │ depicts a man  │ sketch of a    │ portrait of a  │
│                │                │                │                │ wearing a hat  │ man in a dark  │ man wearing a  │
│                │                │                │                │ and coat,      │ hat and coat,  │ wide-brimmed   │
│                │                │                │                │ looking at us. │ with the       │ hat and dark   │
│                │                │                │                │ Depth and      │ inscription "à │ clothing. The  │
│                │                │                │                │ shadows are    │ Bartholomé     │ work is signed │
│                │                │                │                │ emphasized     │ Degas" at the  │ "à Bartholome  │
│                │                │                │                │ through the    │ bottom.        │ Deyas."        │
│                │                │                │                │ dark shade of  │                │                │
│                │                │                │                │ the man's      │                │                │
│                │                │                │                │ clothes and    │                │                │
│                │                │                │                │ the smudged    │                │                │
│                │                │                │                │ background.    │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1947.183       │ 1947.183_web.… │ ../curated_im… │ image/jpeg     │ An armchair    │ [FAIL] An      │ [FAIL] An      │
│                │                │                │                │ features a     │ ornate sofa    │ antique        │
│                │                │                │                │ light-colored  │ upholstered in │ upholstered    │
│                │                │                │                │ floral         │ a detailed     │ bench          │
│                │                │                │                │ tapestry with  │ floral and     │ featuring a    │
│                │                │                │                │ a central      │ bird tapestry, │ floral pattern │
│                │                │                │                │ image of a     │ supported by   │ in soft greens │
│                │                │                │                │ raven peering  │ carved wooden  │ and blues on a │
│                │                │                │                │ down at a      │ legs and a     │ cream          │
│                │                │                │                │ coyote. The    │ decorative     │ background,    │
│                │                │                │                │ wood legs of   │ base.          │ supported by   │
│                │                │                │                │ the armchair   │                │ carved wooden  │
│                │                │                │                │ are            │                │ legs.          │
│                │                │                │                │ intricately    │                │                │
│                │                │                │                │ carved.        │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1958.42        │ 1958.42_web.j… │ ../curated_im… │ image/jpeg     │ A vertically   │ [FAIL]         │ [FAIL]         │
│                │                │                │                │ oriented oil   │ Abstract       │ Close-up of a  │
│                │                │                │                │ painting       │ painting       │ large, pale    │
│                │                │                │                │ depicts a      │ depicting a    │ white petal or │
│                │                │                │                │ close-up of    │ large,         │ leaf structure │
│                │                │                │                │ the center of  │ stylized white │ with soft      │
│                │                │                │                │ a white        │ flower with    │ folds and      │
│                │                │                │                │ flower. In the │ soft, flowing  │ shading,       │
│                │                │                │                │ lower          │ petals and a   │ contrasting    │
│                │                │                │                │ right-hand     │ dark base,     │ against a dark │
│                │                │                │                │ side of the    │ rendered in    │ area at the    │
│                │                │                │                │ painting, soft │ muted tones.   │ bottom.        │
│                │                │                │                │ slopes of      │                │                │
│                │                │                │                │ black petals   │                │                │
│                │                │                │                │ fill the       │                │                │
│                │                │                │                │ corner.        │                │                │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1956.718       │ 1956.718_web.… │ ../curated_im… │ image/jpeg     │ A pastel and   │ [FAIL] A soft, │ [FAIL] A       │
│                │                │                │                │ oil portrait   │ impressionist… │ portrait       │
│                │                │                │                │ depicts the    │ portrait of a  │ painting of a  │
│                │                │                │                │ side profile   │ woman in       │ woman in       │
│                │                │                │                │ of a woman     │ profile, her   │ profile, shown │
│                │                │                │                │ facing our     │ dark hair      │ in a           │
│                │                │                │                │ left. The      │ styled up with │ three-quarter  │
│                │                │                │                │ subject has    │ a braid,       │ view. She has  │
│                │                │                │                │ pink-tinged    │ wearing a      │ dark hair      │
│                │                │                │                │ light skin and │ light-colored  │ pulled back    │
│                │                │                │                │ dark brown     │ lace garment   │ and is wearing │
│                │                │                │                │ hair.          │ and a blue     │ a              │
│                │                │                │                │                │ earring,       │ light-colored  │
│                │                │                │                │                │ against a      │ garment with   │
│                │                │                │                │                │ muted gray     │ delicate lace  │
│                │                │                │                │                │ background.    │ around her     │
│                │                │                │                │                │                │ neck.          │
├────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┼────────────────┤
│ 1983.28        │ 1983.28_web.j… │ ../curated_im… │ image/jpeg     │ A gray-white   │ [FAIL] A round │ [FAIL] A pale, │
│                │                │                │                │ glazed         │ ceramic jar    │ globular       │
│                │                │                │                │ spherical      │ with a pale    │ ceramic vase   │
│                │                │                │                │ porcelain jar  │ green glaze    │ with a smooth  │
│                │                │                │                │ features       │ and subtle     │ surface and    │
│                │                │                │                │ narrow,        │ crackle        │ subtle         │
│                │                │                │                │ circular rims  │ patterns,      │ horizontal     │
│                │                │                │                │ at the base    │ photographed   │ striations.    │
│                │                │                │                │ and mouth.     │ against a      │                │
│                │                │                │                │ Faint,         │ neutral        │                │
│                │                │                │                │ horizontal     │ gradient       │                │
│                │                │                │                │ lines striate  │ background.    │                │
│                │                │                │                │ the jar with   │                │                │
│                │                │                │                │ fine cracks    │                │                │
│                │                │                │                │ webbing the    │                │                │
│                │                │                │                │ surface.       │                │                │
└────────────────┴────────────────┴────────────────┴────────────────┴────────────────┴────────────────┴────────────────┘
... 25 more rows not shown ...

✓ Eval complete (ID: eval-XIJ-2026-09-09T13:41:17)

» View results: promptfoo view
» Share with your team: https://promptfoo.app
» Feedback: https://promptfoo.dev/feedback

Total Tokens: 32,756
  Provider: 32,756 (14,900 prompt, 17,856 completion)

Results:
  0 passed (0%)
  ✗ 100 failed (100%)
  0 errors (0%)
Duration: 9m 42s (concurrency: 1)
```

---