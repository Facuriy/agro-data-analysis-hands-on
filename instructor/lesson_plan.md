# Instructor guide · 90 minutes

## Three outcomes

Students should leave able to:

1. **Design:** identify the experimental unit and choose a method from the outcome, design, and question.
2. **Evaluate:** distinguish a blocked treatment model from a post-treatment ANCOVA, choose a comparison family, and evaluate grouped CNN predictions.
3. **Communicate:** separate numerical Results from interpretation, limits, and next tests.

CNN architecture and basic Python remain in Nathan’s course. The live student
notebook contains figures and four minimal section banners only. Long code
starts collapsed; this guide contains the spoken questions and explanations.
Do not ask students to read paragraphs on screen.

## Before class

Students use **Google Colab**, not a local environment. Send the Colab link in
advance and ask every student to open it while signed into a Google account.
They do not need to clone the repository.

Instructor preflight from a local checkout:

~~~bash
python -m pip install -r requirements.txt
python scripts/build_notebooks.py
python scripts/privacy_audit.py
python scripts/verify_notebooks.py
~~~

Require PASS from all three checks. Run the notebook once in the same local or
Colab environment students will use. In Colab, use **Runtime → Restart session
and run all** once before class. Internet is required because Colab retrieves
the released tables and JPEGs from GitHub.

Class profile: 14 international agronomy students at a German university,
working as seven pairs. Every pair has a laptop and GitHub access. Teaching,
student materials, and projected prompts are entirely in English; mirror the
same notebook on the instructor screen.

Use the student notebook on the projector—not the detailed solutions notebook.
Run all cells once, then move figure by figure. Students should mostly point,
vote, discuss, and state decisions; scrolling text is not part of the lesson.

Read [experiment_context.md](experiment_context.md) before class. The June RGB
descriptor is post-inoculation and shares a date with the first fungicide
application. Present the blocked treatment model as primary and ANCOVA as a
short sensitivity/estimand lesson.

The timeline is generated from `data/field_events.csv`, not typed into the
figure. Its RGB rows were checked against the acquisition inventory and its
fungicide rows against the agronomic application table. Ask students to notice
that the notebook first verifies every recorded date against DAS.

Say:

> These are real observations from a deliberately tiny teaching subset. We can
> learn the workflow from it; the subset cannot replace the full experiment.

## Teaching rhythm

Every section uses:

**predict → discuss → reveal → decide**

Students work in pairs. A reveal is earned only after both students commit to
an answer.

## Run of show

| Min | Activity | Student action |
|---:|---|---|
| 0–2 | Frame | identify the scientific claim boundary |
| 2–8 | Blind RGB detective | choose Image A/B as September and point to evidence |
| 8–13 | Reveal dates + plots | separate observation from evidence |
| 13–16 | Trial timeline | catch the post-treatment-covariate problem |
| 16–21 | Three maps | label descriptor, ordered response, continuous response |
| 21–25 | Mystery plots | predict Inoculated before the treatment reveal |
| 25–29 | Audit | name plot as the experimental unit |
| 29–35 | Method vote + tree | choose blocked model; explain why ANCOVA is conditional |
| 35–38 | Transfer | choose a family for ordinal severity |
| 38–45 | Primary + sensitivity | compare blocked ANOVA with post-treatment ANCOVA |
| 45–53 | Diagnostic jigsaw | one panel per pair; choose OK / WARNING / STOP |
| 53–57 | Class decision | agree on main warning and action |
| 57–61 | Model means | compare raw and block-averaged estimates |
| 61–66 | Post hoc choice | choose family before forest plot |
| 66–69 | Residual map | state why it is not a spatial correction |
| 69–71 | Retrieval pause | close notebook and reconstruct question → model → check → claim |
| 71–75 | Leakage vote | random crops or whole-block holdout |
| 75–81 | CNN evidence | read block dots and confusion matrices |
| 81–86 | Results/Discussion card sort | classify R, D, or Unsupported |
| 86–89 | Two-sentence conclusion | one Results + one Discussion sentence |
| 89–90 | Exit | one permitted and one prohibited claim |

## Facilitation prompts

### Field

- What changed visibly?
- Which clue could be caused by image display stretching?
- What cannot be concluded from a map?

### Model

- What is the experimental unit?
- Was the candidate covariate measured before treatment? What changes when it was not?
- Why does block remain even if its p-value is large?
- If severity is ordered, what changes?

### Diagnostics

Assign one panel to each pair. Require:

1. signal: OK / WARNING / STOP;
2. one visible piece of evidence;
3. one defensible action.

Do not teach Shapiro, Breusch–Pagan, or Cook’s distance as pass/fail gates.
Independence comes from randomization, sampling, and lack of interference.

### Comparisons

Ask the scientific question before naming a test:

- all pairs → Tukey;
- treatments against one control → Dunnett;
- a specified model-contrast family → Holm can control multiplicity.

The lesson uses two specified blocked-model contrasts against Control. The forest
plot contains ordinary model-based 95% intervals and Holm-adjusted p-values;
the intervals are not simultaneous.

### CNN

- What leaks under a random crop split?
- Why are 24 rows not 24 independent field units?
- What do the four block-level dots reveal?
- What error pattern is hidden by accuracy?

Do not calculate a generalization interval from 11/24. The same 12 plots occur
at two dates and the four cross-validation fits share training observations.

## What to cut

Never cut the writing/card-sort integration. If time is short, cut:

1. detailed diagnostic p-values;
2. individual labels on the residual map;
3. macro-F1 discussion;
4. student reporting from more than one pair.

Keep alternative methods as a visual map, not mini-lectures.

## Optional extensions

- [Responsible vibe-coding extension](vibe_coding_extension.md)
- [Classifier-evaluation notebook](../notebooks/evaluate_any_classifier_template.ipynb)
- Nathan’s CNN material as preparation or homework
- external validation design across seasons and cultivars
- formal spatial analysis only with a larger, appropriately released dataset

Pedagogical and statistical sources are collected in [SOURCES.md](../SOURCES.md).
