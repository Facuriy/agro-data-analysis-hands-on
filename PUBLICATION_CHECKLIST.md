# Publication checklist

## Identity

- [x] Confirm repository owner and final name.
- [x] Confirm Facuriy/agro-data-analysis-hands-on for the Colab badge and raw-file fallback.
- [x] Add preferred author name. Affiliation can be added later.
- [x] Confirm the LICENSE copyright holder.
- [x] Add CITATION.cff for the course repository; dataset-paper DOI remains forthcoming.

## Blocking scientific questions

- [x] Document that all 12 Aluco plots were included.
- [x] Document why Aluco was chosen: low resistance to Cercospora leaf spot, not observed outcomes or significance.
- [x] Document treatment timing relative to 2020-06-26 and stop calling June green share a clean baseline.
- [x] Confirm the recorded randomised complete block design.
- [ ] Confirm whether interference between adjacent plots can be treated as negligible.
- [x] Document available measurement units and methods.

## Rebuild and verify

- [x] If rebuilding data, run the separate local private-source builder before entering this public folder.
- [x] Run python scripts/privacy_audit.py and require PASS.
- [x] Run python scripts/build_notebooks.py.
- [x] Run python scripts/verify_notebooks.py and require three PASS messages.
- [x] Execute the student notebook from a clean local environment.
- [x] Execute the student notebook from a clean temporary folder using only public GitHub data/image URLs.
- [x] Open the public student notebook in Colab and confirm that all 27 cells load.

## Visual review

- [x] Confirm that plot boundaries align with both RGB previews.
- [x] Confirm P01, P02, and P03 show three treatments from Block 1.
- [x] Confirm maps, decision trees, diagnostics, forest plot, residual map, and confusion matrices are legible when projected.
- [x] Confirm the compact visual notebook still fits a 90-minute run.

## Release safety

- [x] Only rgb_early_512.jpg and rgb_late_512.jpg are present as image binaries.
- [x] Only field_plots.csv, field_events.csv, cnn_model_outputs.csv, README.md, and the manifest are present in data/.
- [x] Both JPEGs are 512 × 512 RGB and contain no EXIF.
- [x] No GPS, projected coordinates, CRS, source IDs, source filenames, or linkage keys.
- [x] No full-resolution raster, vector dataset, model weights, or cached crop images.
- [x] The real-data teaching notice is visible in README, notebook, data documentation, and asset documentation.
- [x] The non-radiometric JPEG warning is visible.
- [x] Manifest hashes match every released data and image file.
- [x] Confirm data/image redistribution rights in DATA_AND_IMAGE_RIGHTS.md.
- [x] Confirm that the MIT license is not presented as the data/image license.
- [x] Confirm that executed notebook outputs contain no absolute local paths.

## Teaching claims

- [x] Results are described as belonging to the 12-plot subset.
- [x] The blocked treatment model is primary; ANCOVA is labelled a post-treatment sensitivity/estimand lesson.
- [x] CNN predictions are described as grouped cross-validation, not deployment validation.
- [x] CNN total 11/24 has no independence-based generalization interval.
- [x] Nathan’s course remains optional preparation or homework.
- [x] Dataset-paper citation is deferred until public bibliographic details are confirmed.

## Release

- [ ] Create a tagged course release.
- [ ] Archive the exact commit used in class.
