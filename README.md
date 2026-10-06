# From field images to scientific evidence

A practical, hands-on introduction to agricultural data analysis.

The course uses one Google Colab notebook and a small real teaching dataset.
Students move step by step from RGB field images to experimental design,
statistical comparison, model checking, spatial interpretation, CNN evaluation,
and scientific writing.

## Course notebook

### Agricultural Data Analysis: Look → Compare → Evaluate → Discuss

Learn how to:

- explore a real field experiment visually;
- identify treatments, blocks, outcomes and experimental units;
- choose a statistical method from the scientific question;
- understand blocked comparisons and conditional ANCOVA;
- read confidence intervals and post hoc comparisons;
- check assumptions with diagnostic plots;
- evaluate a CNN without spatial leakage;
- separate Results from Discussion.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Facuriy/agro-data-analysis-hands-on/blob/v2.0.0/Agro_Data_Analysis_Field_to_Evidence.ipynb)

## Getting started

1. Open the notebook using the Colab button above.
2. Sign in to a Google account if prompted.
3. Run the cells from top to bottom using ▶ or `Shift + Enter`.
4. Read the short explanations and answer each question before continuing.
5. Use **Runtime → Run all** if you want to reproduce the complete analysis.

No local Python installation is required. The notebook downloads the released
course data automatically.

## What is included

- one self-guided notebook in English;
- all 12 Aluco plots from four blocks and three treatments;
- two real, reduced RGB field previews;
- a ten-event agronomic timeline;
- sugar, root-weight, severity and image-derived teaching variables;
- 24 grouped cross-validation predictions from a small CNN.

The data form a deliberately small educational subset. They are suitable for
learning the analysis workflow, not for replacing the complete experiment or
making claims about other cultivars, fields or seasons.

## Requirements

- a computer with internet access;
- a Google account for Google Colab;
- basic Python familiarity;
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
