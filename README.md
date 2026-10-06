# Agro Data Analysis Hands-on

**Look → compare → evaluate → discuss**

A visual, guided 90-minute practical for agricultural-science students who know basic Python and have already seen CNN theory.

## Start

- [Student notebook](notebooks/field_to_evidence_student.ipynb)
- [Executed notebook with answers](notebooks/field_to_evidence_solutions.ipynb)
- [Instructor guide](instructor/lesson_plan.md)
- [Expected results](instructor/expected_results.md)
- [Optional classifier-evaluation template](notebooks/evaluate_any_classifier_template.ipynb)

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Facuriy/agro-data-analysis-hands-on/blob/main/notebooks/field_to_evidence_student.ipynb)

**Student route:** open the Colab badge and choose **Runtime → Run all**. The
student notebook is a visual lab: four short sections, large figures, and no
reading blocks. The instructor asks the pair questions aloud. No clone or local
Python installation is required.
When opened from Colab, the notebook reads the small released CSV/JPEG files
directly from GitHub.

## The 90-minute path

| Minutes | Students do |
|---:|---|
| 0–15 | Compare two real RGB field previews and reconstruct the trial timeline |
| 15–25 | Map three variables and zoom into three treatments |
| 25–35 | Use a decision tree to choose a statistical method |
| 35–55 | Fit a blocked model; test whether ANCOVA is scientifically defensible |
| 55–65 | Choose post hoc tests and map spatial residuals |
| 65–78 | Evaluate a tiny CNN with grouped cross-validation |
| 78–90 | Write Results separately from Discussion |

The notebook is intentionally figure-first. All implementation code starts
collapsed; explanations and facilitation prompts live in the instructor guide
and the detailed solutions notebook. The 14 students work as seven pairs
through **predict → discuss → reveal → decide** cycles. The notebook and
facilitation are entirely in English and assume each pair has a laptop with
GitHub/Colab access while the instructor mirrors the same visual notebook.

## Released teaching material

This repository includes a **small de-identified real-data subset**:

- all 12 Aluco plots: 4 blocks × 3 treatments;
- 10 dated experiment events used to construct the timeline from data;
- one anonymous plot for each treatment within every block;
- real RGB display previews from 2020-06-26 and 2020-09-03;
- real plot observations used for the guided ANCOVA;
- 24 predictions from a real tiny-CNN run: 12 plots × 2 dates;
- plot boundaries represented only in 512-pixel preview coordinates.

It does **not** include GPS or projected coordinates, a CRS, source plot or experiment IDs, full-resolution rasters, linkage keys, or model weights.

The RGB JPEGs are independently display-stretched previews. Green share is a
display-scale teaching descriptor—not NDVI and not a calibrated cross-date
time series. Aluco was selected for its low resistance to Cercospora leaf spot,
and every Aluco plot in the trial is included. This supports a transparent
within-cultivar analysis but not generalization to other cultivars.

The June RGB image was acquired two days after the recorded canopy-closure
inoculation timing and on the date of the first fungicide application. Because
the within-day order is not documented, June green share is **not a clean
pretreatment baseline**. The primary statistical analysis therefore uses
treatment + block; ANCOVA is shown as a modern sensitivity/estimand lesson,
not as the total causal treatment effect.

See [data/README.md](data/README.md), [assets/README.md](assets/README.md), the
machine-readable manifest, and [data/image rights](DATA_AND_IMAGE_RIGHTS.md).
The software and original teaching documentation use MIT; the released data
and RGB previews have a separate, attributed educational-use permission.

## Local setup

Students and instructors can use the committed release:

~~~bash
python -m pip install -r requirements.txt
python scripts/privacy_audit.py
python scripts/build_notebooks.py
python scripts/verify_notebooks.py
jupyter lab
~~~

The source-to-release builder is intentionally kept **outside this public folder** because it contains private workspace paths and linkage logic. The released tables, images, manifest, and public verification tools are committed here.

## Optional connection to Nathan’s course

[Nathan Okole’s Introduction to Programming](https://github.com/nathanokole/Introduction-to-programming) can remain optional preparation, an extension, or homework. Students may run one of its CNN examples and bring the true labels, predictions, and grouping variable into this notebook’s evaluation workflow.

For an optional AI-assisted activity, use the
[responsible vibe-coding extension](instructor/vibe_coding_extension.md). It
requires assertions and evidence checks and never asks students to upload
private data or use an API key. The classifier template lets students transfer
the evaluation workflow to outputs from Nathan’s CNN or another model.

## Repository map

| Folder | Contents |
|---|---|
| assets | two real, downsampled RGB previews |
| data | de-identified tables, field values, predictions, manifest |
| notebooks | student and executed solution notebooks |
| instructor | timing, prompts, expected values |
| scripts | notebook builder, verification, privacy audit |

Scientific and pedagogical references are collected in [SOURCES.md](SOURCES.md).
The [experiment context](instructor/experiment_context.md),
[release notes and scientific limitations](instructor/open_questions_before_publication.md),
and [release checklist](PUBLICATION_CHECKLIST.md) document the evidence boundary
and quality checks for this course version.
