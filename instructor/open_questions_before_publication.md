# Release notes and remaining scientific questions

The cultivar selection, inclusion rule, timeline, recorded randomised complete
block design, and available measurement provenance are now documented in
[experiment_context.md](experiment_context.md).

## Scientific claim

1. **Interference**  
   Can spread between adjacent plots be treated as negligible for the intended
   treatment-effect interpretation? If not, retain association language and
   explain the possible direction of contamination.

2. **Same-day order**  
   Is there a timestamp or field note establishing whether the 2020-06-26 UAV
   acquisition occurred before or after fungicide application? This cannot turn
   June imagery into a pre-inoculation baseline, but it can sharpen its
   interpretation for the fungicide group.

3. **Severity metadata**  
   Confirm the exact field-score rubric and assessor provenance for the plot
   score used on 2020-09-04 if these are to appear in a public methods section.

4. **Inoculum protocol detail**  
   The recovered records support whole-plot inoculation at canopy closure, but
   not the exact 2020 inoculum material and rate. Do not copy the separately
   documented 2019 rate into this trial without a 2020 source.

## Rights and citation

Resolved on 2026-10-06: the data owner authorized public release of the exact
de-identified educational subset. The repository records an attributed,
non-commercial educational-use permission; it does not license the full data.

5. What DOI or approved citation identifies the forthcoming dataset paper?

## Class logistics

Resolved: teaching is entirely in English; 14 international agronomy students
work in seven pairs; each has a laptop and GitHub access; the instructor mirrors
the notebook on the main screen.

8. Can students edit short pandas/statsmodels lines, or should they mainly run
   and interpret pre-written cells?
9. Is use of an AI assistant permitted by the course and university policy?

## Claim rule

- The primary blocked model supports transparent within-Aluco comparisons in
  this trial; causal language still requires negligible interference and
  confidence in implementation.
- ANCOVA with June green share is a conditional sensitivity analysis, not an
  estimate of the total treatment effect.
- The missing future DOI does not block this owner-authorized course release;
  add it when public bibliographic details become available.
