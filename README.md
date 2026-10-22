# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter classifies public Ask HN posts by their primary communicative intent:
reporting a checkable incident, requesting advice with concrete context, asking
an open question, or stating a position. The dataset contains 200 complete
posts from the public Hacker News Algolia API. I fine-tuned DistilBERT to test
whether those text-level distinctions can be learned from a small labelled
dataset.


---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `case_report`

**Definition:** Describes a discrete incident or external change, supports it
with a checkable detail, and explicitly asks for explanation or action.

**Example 1:**
> AppStore – Waiting for Review  Hello, I've been in the iOS App Review for 4
> days, and I'm wondering what the experience is for others with it; 2 years
> ago, when I submitted a different one, it went through in less than 24
> hours. Is this normal? Or might my app stay more in review for some other
> reason?

**Example 2:**
> Ask HN: Any way to remove ads in Apple apps?  Apple has added notification
> red icons to the Apple Settings app to try to sell extended AppleCare. I find
> this annoying because there are their alerts in the Settings app that I
> immediately respond to. Any tricks to turn these off (without buying the
> service)?

### `worked_request`

**Definition:** Seeks advice for a concrete decision and supplies a material
constraint, prior attempt, rejected option, or success criterion, but is not
primarily investigating a discrete external incident.

**Example 1:**
> Ask HN: Any good technical podcasts to listen to while driving?  It takes me
> 30 to 40 minutes to reach the office every day and would love to listen to a
> technical podcast if such a thing exists. Something that is thorough and not
> hype based.

**Example 2:**
> Ask HN: What are the best open models for computer use?  Playing around with
> Opus 5.5 + Blender has yielded some crazy results, but my $200 plan maxes
> almost instantly. Any open models that are somewhat comparable (maybe like
> 80% as good) right now?

### `open_question`

**Definition:** Directly solicits information or experiences but provides no
material constraint, prior attempt, success criterion, or checkable support
for its premise.

**Example 1:**
> Ask HN: What's your current MacBook wallpaper?  looking for inspo

**Example 2:**
> Ask HN: In the age of AI does your boss still ask you for time estimates?
> See title, just curious.

### `position`

**Definition:** Primarily argues, reacts, announces, promotes, or petitions;
any question is rhetorical or secondary rather than a genuine request for
information or advice.

**Example 1:**
> Ianal?  looks like we've been kidding ourselves all these years prefixing our
> advice with "IANAL". Maybe let's switch to IANAA from now on.

**Example 2:**
> I gained 20k impressions on my LinkedIn profile in 100 days  I gained 20,000
> impressions on my LinkedIn profile in 100 days! Thank you to everyone who
> read, liked, commented and shared my posts!

### The hardest boundary

**Which two labels:** `case_report` and `worked_request`

**The decision rule I used every time:**
<!-- e.g. "If the post names a specific checkable fact, it's `analysis`, even
     if the tone is heated." -->

If a post is primarily investigating a discrete external incident or change
and gives a checkable detail, I use `case_report`; otherwise, a genuine advice
request with a material constraint, attempt, rejected option, or success
criterion is `worked_request`.


---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**

The posts are public Ask HN submissions collected through the public Hacker
News Algolia API. I kept each complete title and text body, skipped submissions
without body text, removed one near-duplicate repost, and did not split the
file. After the first balance check, I replaced seven routine `position` posts
with older `case_report` posts from the same feed so every label met the 15%
minimum I set in `criteria.md`.

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Say so plainly — the disclosure is required, not penalised. -->

I labelled rows 1-20 cold and marked them `cold` in the `note` column. An AI
pre-labelled rows 21-200 in three batches using my definitions and precedence
rule; I then read every complete post, accepted or corrected each suggestion,
and marked those rows `pre-labelled, checked`. Hard cases and their boundary
rules are recorded in the corresponding notes.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `case_report` | 30 | 15.0% |
| `worked_request` | 65 | 32.5% |
| `open_question` | 44 | 22.0% |
| `position` | 61 | 30.5% |
| **Total** | **200** | 100% |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**
> *The post:* “Ask HN: Dark mode for HN please? (2026)”
>
> *Could have been:* `position` or `worked_request`
>
> *I chose, because:* `position`. It argues and petitions HN to add a native
> feature; it does not ask readers for information or advice.

**2.**
> *The post:* “Tell HN: Getting spam after commenting on monthly Who's Hiring
> posts. Who else?”
>
> *Could have been:* `case_report` or `position`
>
> *I chose, because:* `case_report`. The quoted spam message supports a
> discrete incident, and the author genuinely asks whether others experienced
> it and what can be done.

**3.**
> *The post:* “Anthropic Console overcharged my card 100x due to
> internationalization input bug”
>
> *Could have been:* `case_report` or `position`
>
> *I chose, because:* `position`. It documents the incident in detail but ends
> by petitioning Anthropic to act, not by requesting information or advice from
> readers.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Training device:** CPU (`torch 2.14.1+cpu`) in this project's `.venv`; no
GPU or other accelerator was used. This is the hardware context recorded in
`results.json` for the seed 42 run.

**Base model:** `distilbert-base-uncased`

**Settings:** <!-- epochs, learning rate, batch size, seed -->

3 epochs, learning rate `2e-5`, batch size 16, maximum length 128 tokens, and
seed 42.

**Anything I changed from the defaults, and why:**

Nothing. I kept all notebook defaults so this first run is a reproducible
baseline for the three-seed comparison in the next unit.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

139 train / 31 validation / 30 test. The test split contains 4 `case_report`,
10 `worked_request`, 7 `open_question`, and 9 `position` posts. The
`case_report` and `open_question` metrics will be especially sensitive to a
single prediction because both have fewer than about eight test examples.


---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1**

- *What I asked for:* Eight synthetic Ask HN posts placed deliberately on the
  boundaries of my draft taxonomy.
- *What came back:* Cases that mixed checkable evidence with rhetorical
  questions or product advocacy.
- *What I changed:* I added an intent gate: without a genuine request for
  information or advice, the label is `position` even when evidence is present.

**Moment 2**

- *What I asked for:* Suggested labels for rows 21-200 using the four
  definitions and the intent-first precedence rule.
- *What came back:* One suggested label and a brief reason per post, with
  uncertain cases flagged.
- *What I changed:* I read every full post and corrected suggestions where the
  primary communicative intent or incident precedence had been applied too
  loosely. The CSV records the reviewed result, not unchecked AI output.

**Pre-labelling disclosure:**

Rows 1-20 were labelled cold. Rows 21-200 were AI-pre-labelled and then
individually read and checked by me; this is also recorded in each row's
`note` value.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.133 | 0.400 | +0.267 |
| Macro F1 | 0.062 | 0.222 | +0.160 |
| F1 — `case_report` | 0.250 | 0.000 | -0.250 |
| F1 — `open_question` | 0.000 | 0.000 | +0.000 |
| F1 — `position` | 0.000 | 0.364 | +0.364 |
| F1 — `worked_request` | 0.000 | 0.526 | +0.526 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

I predict that the trained model will beat the zero-shot baseline most clearly
on `position`, where training examples should help it distinguish rhetorical or
promotional language from genuine requests.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

On the same 30 held-out posts, fine-tuning added 26.7 percentage points of
accuracy and 0.160 macro F1 over the definitions-based baseline, mainly by
learning `worked_request` and `position`; it still failed to learn
`open_question` and traded away the baseline's `case_report` recall. My
prediction about `position` was supported, though `worked_request` showed the
largest F1 gain. As a prompt ablation, I also ran the baseline with bare label
names: it scored 0.400 accuracy and 0.291 macro F1, versus 0.133 and 0.062 with
the definitions. Thus these definitions were worth -26.7 accuracy points in
this zero-shot setup: rather than helping, they biased 28 of 30 predictions
toward `case_report`.


---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | At least 0.65 in every seed | 0.400 | 0.400 | 0.600 | **MISSED** |
| 2. Per-label F1 | Every label at least 0.50 in every seed | minimum 0.000 | minimum 0.000 | minimum 0.000 | **MISSED** |
| 3. Label balance | Every label 30–90 posts | 30–65 | 30–65 | 30–65 | **MET** |
| 4. Annotation agreement | At least 24/30 | pending | pending | pending | **NOT YET TESTED** |
| 5. Confidence gap | Most-confident third at least 0.20 above least-confident third | +0.400 | +0.300 | +0.000 | **MISSED** |

### Three-seed metric spread

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.400 | 0.400 | 0.600 | 0.200 |
| Macro F1 | 0.222 | 0.218 | 0.467 | 0.249 |
| F1 — `case_report` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 — `worked_request` | 0.526 | 0.541 | 0.600 | 0.074 |
| F1 — `open_question` | 0.000 | 0.000 | 0.444 | 0.444 |
| F1 — `position` | 0.364 | 0.333 | 0.824 | 0.490 |

Accuracy moved 0.200 across seeds, more than ten percentage points. The
30-post test sets are too small for a stable measure, especially for
`case_report` and `open_question`, which have only 4 and 7 test examples per
seed; the 0.400 single-seed result was therefore not a stable estimate.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted | case_report | worked_request | open_question | position |
|---|---|---|---|---|
| **case_report** | 0 | 4 | 0 | 0 |
| **worked_request** | 0 | 10 | 0 | 0 |
| **open_question** | 0 | 7 | 0 | 0 |
| **position** | 0 | 7 | 0 | 2 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

Seven real `open_question` posts were called `worked_request`, while none went
the other way, so the seed-42 model leaned strongly toward advice requests and
did not learn the boundary between unconstrained questions and requests with a
material constraint.


---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
