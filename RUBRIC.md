# Task 1 — Evaluation Rubric

**Domain:** grounded Q&A bot for the Kaplan family task-management system. The
model answers a family member's question using only `family_task_guide.txt`
as its knowledge base, in a warm, helpful household-assistant voice, never
inventing facts. This replaces the assignment's default e-commerce
product-description use case; the "50-90 word product description" shape
becomes "1-3 sentence answer."

This rubric is written before any output has been generated or seen (Task 2),
with one explicit exception the assignment allows: the Latency thresholds
were calibrated from a couple of throwaway timing runs on the local model,
since there was no other way to know the rough scale on this machine.

---

## 1. Fluency — do the sentences read naturally, like a person wrote them?

| Rating | Definition |
|---|---|
| good | No awkward phrasing anywhere in the answer; reads the way a person would naturally speak to a family member. |
| ok | 1-2 clunky or stiff phrases, but the meaning is clear throughout and nothing needs re-reading. |
| bad | 3+ awkward phrases, or at least one sentence you have to re-read to parse, or the sentence structure is broken/garbled. |

## 2. Grammar — correct spelling, punctuation, agreement?

| Rating | Definition |
|---|---|
| good | No spelling, punctuation, or agreement errors. |
| ok | 1-2 minor errors (a missing comma, a small typo, a subject-verb slip) that do not obscure the meaning. |
| bad | 3+ errors, or any single error that changes or obscures the meaning, or the response is a sentence fragment presented as a complete answer. |

## 3. Tone — does it match a warm, helpful family-assistant voice?

(Adapted from the assignment's "friendly, credible sales voice" — here the
voice is a household assistant talking to a family member, not a salesperson
talking to a customer.)

| Rating | Definition |
|---|---|
| good | Sounds like a warm, helpful household assistant speaking directly to the family member who asked; friendly without being gushing; no sales/marketing language. |
| ok | Tone is present but flat/robotic (reads like a FAQ entry), OR mildly over-enthusiastic (exclamation points, "Great question!"), but not actively off-putting. |
| bad | Cold, robotic recitation of facts with no warmth at all, OR reads like sales/marketing copy ("Don't miss out on staying organized!"), OR is condescending/preachy toward the person asking. |

## 4. Length — target is a 1-3 sentence answer

(Adapted from the assignment's "50-90 words" — see the assignment's own
suggested substitution for the grounded-QA shape: "answers in 1-3
sentences.")

| Rating | Definition |
|---|---|
| good | 1-3 sentences AND 10-60 words. |
| ok | 4 sentences, OR 61-90 words (any sentence count), OR 1-3 sentences but fewer than 10 words when the question clearly warranted a fuller answer. |
| bad | 0 sentences (empty or a non-answer), OR 5+ sentences, OR more than 90 words, OR the response is formatted as a bulleted/numbered list instead of prose. |

## 5. Grounding — does it stick to `family_task_guide.txt`, inventing nothing?

**This is the safety criterion.** A beautifully written answer that invents a
policy the document never stated is a worse failure than a clumsy but
truthful one.

Ruling on generic filler: a general, non-factual pleasantry ("communication
matters in a household like this one") is acceptable and does **not** count
against grounding, as long as it never asserts a specific system rule,
feature, or behavior that isn't in the document. The moment filler starts
making a claim about how the *system* works, it's a grounding claim and must
be checked against the text.

| Rating | Definition |
|---|---|
| good | Every factual claim about the system is directly stated in or a faithful paraphrase of `family_task_guide.txt`. If the question's answer is not in the document, the response declines using (or closely matching) the required sentence: "I can't find that in the document." |
| ok | Grounded overall, but adds one minor, non-policy embellishment not stated in the text (e.g. an invented but plausible example) that doesn't change the substance of the answer, OR the refusal is used but only after first offering a speculative guess. |
| bad | States a specific policy, rule, feature, or fact about the system that does not appear in `family_task_guide.txt` (fabrication), OR fails to decline when the question is genuinely out of the document's scope and invents an answer instead. |

## 6. Latency — time per call (ms), measured programmatically

Thresholds calibrated from 3 real local-model timing runs (`Qwen/Qwen2.5-0.5B-Instruct`,
CPU inference, this machine, `max_new_tokens=150`) before Task 2's full
generation run: observed 12,151 / 13,392 / 18,287 ms. **Latency is measured,
not judged** — it is never sent to the LLM judge in Task 5, and its value
comes straight from the timer around each generation call.

| Rating | Definition |
|---|---|
| good | ≤ 15,000 ms |
| ok | 15,001–25,000 ms |
| bad | > 25,000 ms |

---

## Pass / Fail

**Go/no-go rule (checked first, overrides everything else):** if **Grounding**
is not rated `good`, the row is an automatic **fail** — a beautifully written,
fluent, perfectly-toned answer that fabricates a policy still fails.

**Cumulative pass bar (only reached if Grounding is `good`):** at least
**4 of the remaining 5 criteria** (Fluency, Grammar, Tone, Length, Latency)
are rated `good`, **and none of them** are rated `bad`. Otherwise the row is
a **fail**.

```
if Grounding != "good":
    final_score = "fail"
else:
    good_count = count of {Fluency, Grammar, Tone, Length, Latency} rated "good"
    bad_count  = count of {Fluency, Grammar, Tone, Length, Latency} rated "bad"
    final_score = "pass" if (good_count >= 4 and bad_count == 0) else "fail"
```

These exact rules are applied identically in Task 3 (by hand), Task 4 (after
each improvement experiment), and Task 6 (by the LLM judge) — see
`scoring.py`.
