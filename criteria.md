# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1.

**In `results_three_seeds_before.json` produced by section 6 of
`takemeter.ipynb`, the `accuracy` value for each of seeds 42, 7, and 2024 is
at least 0.65. Section 6's unchanged `split_dataset` function defines each
held-out set using its stratified 70/15/15 split.**

**Why this target:**

A four-label random guesser would average about 0.25 accuracy, so 0.65 would be
a substantial improvement and would make the classifier right on roughly two
out of every three posts. I did not set it higher because the taxonomy has two
close boundaries (`case_report`/`worked_request` and
`open_question`/`position`) and each seed tests only about 30 of the 200 posts.

---

## 2.

**In `results_three_seeds_before.json` produced by section 6 of
`takemeter.ipynb`, every label's `per_label` F1 value is at least 0.50 for each
of seeds 42, 7, and 2024. The notebook's unchanged `evaluate` function is the
scoring procedure, including its `zero_division=0` convention.**

**Why this target:**

Overall accuracy could hide a model that ignores a less common label. An F1
floor of 0.50 requires useful precision and recall for every label, while
allowing for the large score jumps caused by having only about five to eight
held-out examples of a label in a 30-post test split.

---

## 3.

**In the final 200-post labelled dataset, every label contains at least 30
posts (15%) and no label contains more than 90 posts (45%).**

**Why this target:**

Thirty examples gives even the smallest label a chance to contribute about
four or five examples to each stratified test split. The 45% ceiling prevents
the model from appearing successful by repeatedly predicting one dominant
kind of Ask HN post.

---

## 4.

**A second annotator, working from the written taxonomy without seeing my
labels, agrees with at least 24 of my labels on 30 posts selected from the
final row-ordered `labels.csv` by
`pandas.DataFrame.sample(n=30, random_state=42)` (at least 80% exact
agreement). I will save the sampled text, my label, and the second label in
`annotation_audit.csv`; exact string matches count as agreements.**

**Why this target:**

The intent gate and precedence rule are meant to make the four labels
repeatable, not merely understandable to me. Requiring 24 of 30 matches allows
at most six disagreements for the genuinely close boundaries while still
showing that another person can apply the rules consistently.

---

## 5.

**For each of seeds 42, 7, and 2024 in `results_three_seeds_before.json`,
`confidence.accuracy_most_confident_third` is at least 0.20 higher than
`confidence.accuracy_least_confident_third`. These fields are calculated by
the notebook's unchanged `confidence_report` function from maximum softmax
probability, using its existing sorting, third-size, and tie behavior.**

**Why this target:**

Confidence is only useful if it helps identify predictions that need review.
With a roughly 30-post test set, each third contains about ten posts, so a
20-point gap means the high-confidence group contains at least two more
correct predictions than the low-confidence group.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
