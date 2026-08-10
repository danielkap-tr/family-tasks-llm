# Reflections

## 1b: which change had the biggest effect on the output, and why?

Of the three changes (system prompt, temperature, structured output), the
**system prompt** had the biggest effect on the actual content and style of
the reply. Giving the model a pirate persona changed almost every word of
the response, while temperature only changed *wording/phrasing* between
runs of the same prompt (0 gave two near-identical replies, 1 gave two
noticeably different ones) without changing the underlying content or
format. The system prompt controls *what kind of answer* the model thinks
it's supposed to give; temperature only controls how much randomness is
injected while generating that same kind of answer.

A separate, arguably more important lesson came from the structured-output
part: even with an explicit "no markdown, raw JSON only" instruction in the
system prompt, the model still wrapped its reply in a ` ```json ... ``` `
code fence the first time it was run. The instruction reduced the chance of
that happening but didn't eliminate it — the code needed a defensive
`strip_code_fence()` step before `json.loads`/Pydantic could parse the
reply reliably. The takeaway: a system prompt shapes behavior, it doesn't
guarantee it — code that consumes LLM output should never assume the model
will always follow formatting instructions exactly.

## 1c: why does forcing a quote and allowing "I don't know" reduce hallucination?

Requiring an exact quote forces the model to point at real text in the
document instead of freely composing an answer from its own general
knowledge. A fabricated answer is much harder to fabricate *convincingly*
once it also has to come with a specific, checkable snippet of the source
— there's no plausible "invented quote" that also happens to appear
verbatim in the file, so the quoting requirement makes it much more likely
the model will either find real supporting text or fail to find one, with
few good places to bluff in between.

Explicitly allowing "I can't find that in the document" removes the
pressure to always produce *some* answer. Without that permission, a model
asked a question it can't ground in the given text has only one path
forward — guess — because refusing was never presented as an acceptable
outcome. Giving refusal equal status as a valid response means the model
doesn't have to choose between "make something up" and "fail the task."

## Closed vs. open

**Closed (Claude via the Anthropic API):** Easy — a handful of lines of
Python got a fast, coherent, instruction-following reply, and the
structured-output exercise (system prompt + Pydantic) worked well once the
markdown-fence quirk was handled. It cost real money and setup: the first
call failed until a payment method/credits were added to the Anthropic
Console, the file/question content in Exercise 1c leaves the machine and is
sent to Anthropic's servers, and every run is a metered, rate-limited API
call rather than something free to repeat endlessly.

**Open (local Hugging Face, Qwen2.5-0.5B-Instruct):** The gain was real
independence — no API key, no billing, nothing leaves the machine, and
after the one-time ~1GB download it runs fully offline with no rate limit
and no per-call cost. What was paid for that: a noticeably weaker and even
factually wrong answer (it claimed gluten-free pizza isn't possible), a
slower response than the hosted call despite the model being tiny, and
extra one-time setup cost (large download, CPU/RAM usage) that the hosted
API never required at all.
