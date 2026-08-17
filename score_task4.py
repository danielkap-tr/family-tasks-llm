"""Task 4 — score all three Claude experiment files and write a comparison summary."""

import pandas as pd
from scoring import final_score

LATENCY_THRESHOLDS = {"good": 15_000, "ok": 25_000}


def latency_rating(ms: float) -> str:
    if ms <= LATENCY_THRESHOLDS["good"]:
        return "good"
    if ms <= LATENCY_THRESHOLDS["ok"]:
        return "ok"
    return "bad"


# fmt: off
# Scores for each experiment, keyed by (experiment, id).
# All Claude answers were read against RUBRIC.md and family_task_guide.txt.
# ID 21: doc mentions same-day = morning of due date; question asks about 11pm
#         tonight for a task due tomorrow — answer correctly says "I can't find
#         that in the document" (the doc has no quiet-hours rule), which is the
#         right grounded refusal. Grounding = good.
# ID 22/23: correct out-of-scope refusals; minor fabricated scope description
#            ("household chores, errands…") not in doc → Grounding = ok.

SCORES_04A = {
    1:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    2:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    3:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    4:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    5:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    6:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    7:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    8:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    9:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    10: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    11: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    12: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    13: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    14: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    15: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    16: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    17: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    18: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    19: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    20: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    # ID 21: correct refusal but appended explanation that mentions "9 PM–7 AM" quiet hours — not in doc
    21: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "bad",  "Grounding": "bad"},
    # ID 22/23: correct refusal but adds invented scope list
    22: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "bad",  "Grounding": "ok"},
    23: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "bad",  "Grounding": "bad"},
    24: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
}

SCORES_04B = {
    1:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    2:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    3:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    4:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    5:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    6:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    7:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    8:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    9:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    10: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    11: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    12: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    13: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    14: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    15: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    16: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    17: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    # ID 18: says "you should delete it" — but doc says deletion for "created by mistake"; answer is correct
    18: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    # ID 19: "I'm sorry" is mild tone inflation; still grounded
    19: {"Fluency": "good", "Grammar": "good", "Tone": "ok",   "Length": "ok",   "Grounding": "good"},
    20: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    # ID 21: same quiet-hours fabrication as 04A
    21: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "bad",  "Grounding": "bad"},
    22: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "ok"},
    23: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "ok"},
    24: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
}

SCORES_04C = {
    1:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    2:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    3:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    4:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    5:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    6:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    7:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    8:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    9:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    10: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    11: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    12: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    13: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    14: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    15: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    16: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    17: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    # ID 18: says "delete it" — correct per doc (task created by mistake)
    18: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    19: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "good"},
    20: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
    # ID 21: same quiet-hours fabrication
    21: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "bad",  "Grounding": "bad"},
    22: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "ok"},
    23: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",   "Grounding": "ok"},
    24: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
}
# fmt: on

EXPERIMENTS = [
    ("assignment_04a.xlsx", SCORES_04A, "04A"),
    ("assignment_04b.xlsx", SCORES_04B, "04B"),
    ("assignment_04c.xlsx", SCORES_04C, "04C"),
]

SCORE_COLS = ["Fluency", "Grammar", "Tone", "Length", "Grounding", "Latency", "final_score"]


def score_df(df: pd.DataFrame, scores: dict) -> pd.DataFrame:
    df[SCORE_COLS] = df[SCORE_COLS].astype(object)
    for _, row in df.iterrows():
        rid = int(row["id"])
        s = scores[rid].copy()
        s["Latency"] = latency_rating(row["latency_ms"])
        s["final_score"] = final_score(s)
        for col, val in s.items():
            df.loc[df["id"] == rid, col] = val
    return df


def main() -> None:
    summary = []
    for path, scores, label in EXPERIMENTS:
        df = pd.read_excel(path)
        df = score_df(df, scores)
        df.to_excel(path, index=False)

        pass_count = (df["final_score"] == "pass").sum()
        fail_count = (df["final_score"] == "fail").sum()
        grounding_fails = (df["Grounding"] != "good").sum()
        latency_bad = (df["Latency"] == "bad").sum()
        summary.append((label, pass_count, fail_count, grounding_fails, latency_bad))
        print(f"{label}: {pass_count} pass / {fail_count} fail  "
              f"(grounding_fail={grounding_fails}, latency_bad={latency_bad})")

    print("\n── Comparison vs Task 3 baseline (0 pass / 24 fail) ──")
    print(f"{'Exp':>4}  {'Pass':>4}  {'Fail':>4}  {'Gnd_fail':>8}  {'Lat_bad':>7}")
    print(f"{'03':>4}  {'0':>4}  {'24':>4}  {'16':>8}  {'24':>7}  ← Qwen baseline")
    for label, p, f, g, l in summary:
        print(f"{label:>4}  {p:>4}  {f:>4}  {g:>8}  {l:>7}")


if __name__ == "__main__":
    main()
