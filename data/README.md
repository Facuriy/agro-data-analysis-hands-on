# Teaching data

Small de-identified real-data subset for one 90-minute class.

## field_plots.csv

All twelve plots from cultivar Aluco: 4 blocks × 3 treatments. Aluco was chosen
for its low resistance to Cercospora leaf spot, independently of the released
sugar values, RGB appearance, or statistical significance. The subset therefore
answers a within-Aluco teaching question; it is not representative of all
cultivars.

| Field | Meaning |
|---|---|
| plot_id | anonymous ID P01–P12 |
| block | block 1–4 |
| treatment | Control, Fungicide, or Inoculated |
| early_green_share | green-pixel share from the June display preview; post-inoculation and same date as the first fungicide application, so not a clean baseline covariate |
| late_green_share | green-pixel share from the September display preview |
| severity_sep04 | real ordinal plot field score from 2020-09-04 |
| root_weight | root weight after washing, kg |
| sugar_content_pct | sugar content, %, measured polarimetrically with aluminium sulfate clarification (ICUMSA GS6-3; Betalyser) |
| pixel_x, pixel_y | centroid in the 512-pixel preview only |
| polygon_early_px, polygon_late_px | real plot shape transformed into preview-pixel space |

Green share is derived from independently stretched JPEG previews. It is **not a radiometric vegetation index** and should not be interpreted as a calibrated change between dates.

## cnn_model_outputs.csv

Twenty-four held-out predictions from a deterministic tiny CNN:

- 12 real plot crops × 2 real RGB dates;
- treatment is the three-class target;
- one complete field block is held out in each fold;
- no crops from the test block enter that fold’s training data.

| Field | Meaning |
|---|---|
| sample_id | anonymous case ID S01–S24 |
| plot_id | anonymous plot ID |
| date | RGB date |
| held_out_block | grouped cross-validation fold |
| true_class | treatment reference |
| cnn_prediction | held-out prediction |
| cnn_confidence | largest predicted class probability |

The table is for evaluation practice, not a benchmark or deployable model claim.
The 24 rows are repeated views of 12 plots, not 24 independent field units.

## field_events.csv

Ten de-identified dated events used to build the experiment timeline in Colab.
Sowing, canopy closure, fungicide applications, and harvest come from the
agronomic records; RGB dates come from the acquisition inventory; the first
grade ≥2 and the classroom severity date come from the severity records.

The notebook checks `days_after_sowing` from the dates before drawing the
timeline. The two 26 June rows intentionally remain separate in the table:
their date overlap is evidence, not a label embedded only in a figure.

## Release constraints

- No GPS, projected coordinates, or CRS.
- No source experiment or plot identifiers.
- No source filenames or linkage key.
- No full-resolution rasters.
- No trained model weights.
- Only two 512 × 512 RGB JPEG previews.

`TEACHING_DATA_MANIFEST.json` records the approved release files and SHA-256
hashes. Release verification and rebuild tools are maintained separately from
the student-facing course repository.

Copyright, attribution, and educational-use terms are recorded in
[DATA_AND_IMAGE_RIGHTS.md](../DATA_AND_IMAGE_RIGHTS.md).
