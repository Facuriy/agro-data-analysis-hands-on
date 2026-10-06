# Responsible vibe coding · optional 10–15 minutes

Use AI as a draft partner whose output must pass scientific checks. Do not add
an API, key, chatbot, or private data to the notebook.

## Rule

**Prompt → predict output → run → verify rows and numbers → inspect claim**

The student—not the assistant—owns the question, design, and conclusion.

## Challenge A · code, predict, verify

Before asking for code:

~~~python
assert len(cnn) == 24
assert cnn.groupby("date").size().eq(12).all()
~~~

Prompt:

> Write pandas/scikit-learn code that computes accuracy and macro-F1 by date
> from dataframe cnn. Do not modify cnn. Return one tidy table.

Verification:

- June must contain 12 rows and 4 correct predictions.
- September must contain 12 rows and 7 correct predictions.
- Total 11/24 is descriptive because the same 12 plots occur twice.

## Challenge B · red-team a bad analysis

Prompt:

> We have 12 plots, 4 blocks, 3 treatments, continuous sugar, and a candidate
> numeric covariate. Propose an analysis. First identify the experimental unit,
> grouping, estimand, whether the covariate could be post-treatment,
> assumptions, and comparison family. Do not invent results.

Find:

1. one correct idea;
2. one missing design fact;
3. one claim that needs verification.

## Challenge C · constrained scientific writing

Prompt:

> Draft one Results sentence from the contrast table. Include direction,
> magnitude in percentage points, the ordinary 95% model interval, and the
> Holm-corrected p-value. Do not claim mechanism, causality, or generalization.

Check every phrase against a table or figure. Move interpretation and next
steps to Discussion.

## Challenge D · accessible plotting

Prompt:

> Refactor this treatment plot so categories differ by marker and line style as
> well as color. Preserve every row, value, axis, and numerical result.

Verify the data hash, row count, labels, and numerical outputs before accepting
the visual change.

## Privacy boundary

- Use only the released CSV files.
- Never paste private paths, raw identifiers, full-resolution imagery, or
  unreleased metadata into an AI service.
- Run python scripts/privacy_audit.py after any generated edit.
- Generated code is not evidence until it executes and reproduces expected
  values.
