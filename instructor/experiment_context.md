# Experiment context for the class

This is the minimum context students need. The public teaching files remain
de-identified and omit the source experiment and plot identifiers.

## Design

- Randomised complete block field trial.
- Two cultivars × three treatments × four blocks in the source trial.
- Crop spacing was 48 cm between rows and 18 cm between plants.
- This teaching subset contains **every Aluco plot**: 12 plots = 3 treatments ×
  4 blocks.
- Aluco was selected because of its **low resistance (susceptibility) to
  Cercospora leaf spot**, not because of the observed outcomes.
- Teaching treatment labels are Control, Fungicide, and Inoculated. Fungicide
  and inoculation are not combined in this three-treatment subset.

## Recorded timeline

| Event | Date | Days after sowing |
|---|---:|---:|
| Sowing | 2020-04-06 | 0 |
| First source RGB acquisition | 2020-04-17 | 11 |
| Canopy closure; source documentation places whole-plot inoculation at canopy closure | 2020-06-24 | 79 |
| June RGB shown in class | 2020-06-26 | 81 |
| Fungicide application 1; product/dose absent from the source record | 2020-06-26 | 81 |
| First grade ≥2 in the source severity series | 2020-07-29 | 114 |
| Fungicide application 2 | 2020-08-05 | 121 |
| Fungicide application 3 | 2020-09-01 | 148 |
| September RGB shown in class | 2020-09-03 | 150 |
| Field severity score used in class | 2020-09-04 | 151 |
| Harvest | 2020-10-23 | 200 |

The timeline is a scientific decision tool. June green share was measured two
days after canopy closure/inoculation timing and on the first fungicide date.
The available records do not establish whether the UAV flight preceded or
followed that day’s application. It must therefore **not** be called a clean
pretreatment baseline.

## Measurements used in the subset

| Variable | Provenance and unit |
|---|---|
| Root weight | Root weight after washing, kg; one source sample per plot in this trial |
| Sugar content | %, polarimetric measurement with aluminium sulfate clarification; ICUMSA GS6-3, Betalyser |
| Severity | Ordinal plot field score on 2020-09-04; treat as ordered rather than interval-scaled |
| Green share | Mean chromatic-green descriptor from a display-stretched 512-pixel JPEG; neither NDVI nor a calibrated cross-date measure |

## Statistical consequence

The primary model is `sugar content ~ treatment + block`. It respects the
recorded blocked design and does not condition the treatment contrast on a
post-treatment image descriptor.

ANCOVA with June green share is retained as a short sensitivity demonstration:
it asks a different, conditional association question. It does not estimate
the total treatment effect. Any causal language also depends on treatment
implementation, randomization integrity, and negligible interference between
plots.

## Source boundary

The dates and design above were reconciled from the source field-protocol
extracts, MIAPPE study metadata, management tables, acquisition inventory, and
the audited dataset manuscript. Exact source paths and private identifiers are
kept outside this public teaching repository.
