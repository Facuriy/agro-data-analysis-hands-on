# Evidence Lab: the susceptible variety

A visual, hands-on introduction to agricultural data analysis for students
without programming experience.

The course uses one Google Colab notebook and a small real teaching dataset.
Students make predictions, alter the analysis, and inspect what breaks. The
activities include treatment identification from real RGB crops,
pseudoreplication, an exact randomization test, leave-one-plot-out sensitivity,
correlation within and between groups, spatial checks, and optional CNN evaluation.

## Course notebook

### Image → Unit → Randomize → Compare → Break → Check → Defend

Learn how to:

- explore a real field experiment visually;
- identify treatments, blocks, outcomes and experimental units;
- choose a method from the question, outcome, design and timing;
- understand a blocked comparison and an ANCOVA sensitivity check;
- read differences and confidence intervals;
- check a model using three visual diagnostics;
- see how pseudoreplication creates fake precision;
- enumerate all 1,296 treatment assignments permitted by the block design;
- evaluate a CNN using grouped rather than leaky splits;
- separate Results from Discussion.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Facuriy/agro-data-analysis-hands-on/blob/v2.2.1/Agro_Data_Analysis_Field_to_Evidence.ipynb)

## Getting started

1. Open the notebook using the Colab button above.
2. Sign in to a Google account if prompted.
3. Run the cells from top to bottom using ▶.
4. Use the dropdowns and sliders before revealing each result.
5. Do not use **Run all** during class: the prediction–experiment–reveal order is intentional.

No local Python installation is required. The notebook downloads the released
course data automatically.

## What is included

- one self-guided notebook in English;
- all 12 plots of one susceptible variety from four blocks and three treatments;
- two real, reduced RGB field previews;
- a ten-event agronomic timeline;
- sugar, root-weight, severity and image-derived teaching variables;
- 24 grouped cross-validation predictions from a small CNN;
- a small versioned helper module used by the single student notebook.

The data form a deliberately small educational subset. They are suitable for
learning the analysis workflow, not for replacing the complete experiment or
making claims about other cultivars, fields or seasons.

## Requirements

- a computer with internet access;
- a Google account for Google Colab;
- no previous programming experience;
- curiosity about agricultural experiments and scientific evidence.

## Related course

This lesson complements
[Nathan Okole’s Python for Agricultural Sciences](https://github.com/nathanokole/Introduction-to-programming),
especially the Basic CNN notebook. CNN architecture is not taught again here;
the focus is on honest evaluation and scientific interpretation.

## Data and image note

The RGB images are real 512-pixel display previews and are not radiometric
products. The repository contains no GPS coordinates, CRS, full-resolution
rasters, source plot identifiers or model weights.

Software and original teaching text use the MIT License. The released data and
images have separate attributed educational-use terms in
[DATA_AND_IMAGE_RIGHTS.md](DATA_AND_IMAGE_RIGHTS.md).

Developed by **Facundo R. Ispizua Yamati** for agricultural science education.
