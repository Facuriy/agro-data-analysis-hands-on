# Expected results

These values describe all 12 Aluco plots in the teaching subset. Aluco was
selected for low Cercospora resistance, so conclusions remain within cultivar
and trial. The recorded design is a randomised complete block design; causal
language additionally requires negligible interference and faithful treatment
implementation.

## Audit

- 12 plots, 4 blocks, 3 treatments, 0 missing values.
- Every block contains one Control, one Fungicide, and one Inoculated plot.
- The plot is the experimental unit.
- June green share is post-inoculation and its date coincides with fungicide
  application 1; it is not a clean pretreatment covariate.

Raw sugar summaries:

| Treatment | n | Mean | SD |
|---|---:|---:|---:|
| Control | 4 | 18.131 | 0.175 |
| Fungicide | 4 | 18.799 | 0.081 |
| Inoculated | 4 | 16.514 | 0.200 |

## Primary blocked model

Model:

~~~text
sugar content ~ treatment + block
~~~

Type II tests:

| Term | df | F | p |
|---|---:|---:|---:|
| Treatment | 2 | 299.524 | 0.000001 |
| Block | 3 | 2.195 | 0.1896 |
| Residual | 6 | — | — |

R² = 0.990; adjusted R² = 0.982. A high fit in twelve selected plots is not
external validation or evidence of a biological mechanism.

Diagnostic aids:

| Aid | p |
|---|---:|
| Breusch–Pagan F version | 0.643 |
| Shapiro–Wilk | 0.044 |

These values do not certify assumptions. Students should mention n = 12, six
residual degrees of freedom, the Q–Q warning, influential P05/P12, and design
knowledge.

Block-averaged model means (equal to raw means in this balanced design):

| Treatment | Mean | 95% CI |
|---|---:|---:|---:|
| Control | 18.131 | 17.965–18.297 |
| Fungicide | 18.799 | 18.633–18.965 |
| Inoculated | 16.514 | 16.348–16.680 |

Specified model contrasts:

| Contrast | Difference | 95% CI | Holm p |
|---|---:|---:|---:|
| Fungicide − Control | +0.668 | +0.433 to +0.902 | 0.000439 |
| Inoculated − Control | −1.618 | −1.852 to −1.383 | 0.000006 |

Differences are **percentage points**. Report direction, magnitude, interval,
and adjusted p—not p alone. Intervals are ordinary model-based 95% intervals;
p-values are Holm-corrected for the specified two-comparison family.

## ANCOVA sensitivity lesson

Adding centred June green share gives treatment F(2,5) = 260.776, p = 0.000009;
green-share p = 0.608, and the treatment × green-share slope test p = 0.526.
The numerical treatment estimates change little, but that does not make the
covariate valid. Conditioning on a post-treatment measurement changes the
question and can bias a total-effect estimate. Present this model only as a
conditional sensitivity analysis.

## CNN evaluation

Real plot crops, treatment target, leave-one-block-out grouped cross-validation:

| Date | Correct | Accuracy | Macro-F1 |
|---|---:|---:|---:|
| 2020-06-26 | 4/12 | 0.333 | 0.256 |
| 2020-09-03 | 7/12 | 0.583 | 0.544 |
| Descriptive total | 11/24 | 0.458 | 0.407 |

Minimum acceptable decision:

- June is at the three-class chance reference.
- Observed accuracy is higher in September, but this does not establish a date effect.
- The 24 rows repeat 12 plots and only four blocks are independently held out.
- Overall performance does not demonstrate validity, calibration, transportability, or deployment readiness.
- More independent blocks, cultivars, dates, seasons, and acquisition conditions are needed.

## Results / Discussion boundary

Supported Results:

- fitted blocked-model treatment test, model means, specified contrasts, intervals;
- grouped-CV CNN scores and confusion matrices.

Discussion only:

- biological interpretation;
- limitation to a low-resistance cultivar;
- possible interference, spatial, or acquisition explanations;
- what the next experiment or validation must test.

Not supported:

- a mechanism;
- claims about the complete paper dataset;
- calibrated temporal inference from JPEG green share;
- a total causal effect from the post-treatment ANCOVA;
- CNN deployment or cross-domain generalization.
