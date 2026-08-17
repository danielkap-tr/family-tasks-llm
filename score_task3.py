"""Task 3 — human scores applied programmatically.

Each rating was determined by reading the generated answer against RUBRIC.md
and family_task_guide.txt. Latency is computed from the measured ms value.
"""

import pandas as pd
from scoring import final_score

# fmt: off
SCORES = {
    # id: {Fluency, Grammar, Tone, Length, Grounding}
    # Latency is derived from latency_ms below.

    # ID 1 — invents "parental guidance/supervision" advice not in doc; too long (5 sentences)
    1:  {"Fluency": "ok",  "Grammar": "good", "Tone": "ok",  "Length": "bad",  "Grounding": "bad"},

    # ID 2 — correct, concise, grounded
    2:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},

    # ID 3 — says "his name as responsible" but then says "you are responsible" — contradicts itself
    3:  {"Fluency": "ok",  "Grammar": "ok",  "Tone": "good", "Length": "ok",   "Grounding": "ok"},

    # ID 4 — "Yes, you don't need..." is a self-contradiction; but grounding is correct (description optional)
    4:  {"Fluency": "bad", "Grammar": "bad", "Tone": "ok",  "Length": "ok",   "Grounding": "good"},

    # ID 5 — says "system allows leaving blank" — doc says the OPPOSITE (must pick a date)
    5:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",  "Grounding": "bad"},

    # ID 6 — says "yes you can assign to both" — doc says max 1 person, split into 2 tasks
    6:  {"Fluency": "good", "Grammar": "good", "Tone": "ok",  "Length": "bad",  "Grounding": "bad"},

    # ID 7 — says "yes recurring is possible" — doc says recurring is NOT supported yet
    7:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",  "Grounding": "bad"},

    # ID 8 — says default is "morning of due date" (same-day) — doc says default is "one day before"
    8:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",  "Grounding": "bad"},

    # ID 9 — says "one week before" — correct per doc for a family trip
    9:  {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "ok",  "Grounding": "good"},

    # ID 10 — correct (no repeated reminders), but adds unsupported "follow up promptly" advice
    10: {"Fluency": "good", "Grammar": "good", "Tone": "ok",  "Length": "ok",  "Grounding": "ok"},

    # ID 11 — invents "email or SMS notification" and "completed history view for current season" (fabricated details)
    11: {"Fluency": "ok",  "Grammar": "good", "Tone": "ok",  "Length": "bad",  "Grounding": "bad"},

    # ID 12 — "completed history view" is a real doc fact; answer is correct and grounded
    12: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},

    # ID 13 — says siblings CAN close tasks — doc says only creator/responsible person can
    13: {"Fluency": "ok",  "Grammar": "ok",  "Tone": "ok",  "Length": "bad",  "Grounding": "bad"},

    # ID 14 — says "retained for current season only" — correct per doc
    14: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},

    # ID 15 — says "removed permanently" — doc says kept for current season, not permanently removed
    15: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "bad"},

    # ID 16 — invents "doesn't affect reminder settings" — doc doesn't state this
    16: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "bad",  "Grounding": "ok"},

    # ID 17 — invents "new responsible person listed as creator" — doc says no assignee history is kept
    17: {"Fluency": "ok",  "Grammar": "ok",  "Tone": "good", "Length": "ok",  "Grounding": "bad"},

    # ID 18 — misreads the question; rambles about editing vs done without answering clearly
    18: {"Fluency": "bad", "Grammar": "ok",  "Tone": "ok",  "Length": "ok",  "Grounding": "ok"},

    # ID 19 — invents "unless manually reviewed by a human" — doc says no undo, period
    19: {"Fluency": "ok",  "Grammar": "good", "Tone": "good", "Length": "ok",  "Grounding": "bad"},

    # ID 20 — says app "will automatically add" tasks from email — doc says a human must confirm, nothing auto-added
    20: {"Fluency": "ok",  "Grammar": "good", "Tone": "ok",  "Length": "bad",  "Grounding": "bad"},

    # ID 21 — invents "Remember for Today" button — doc says same-day reminder goes out morning of due date
    21: {"Fluency": "ok",  "Grammar": "good", "Tone": "ok",  "Length": "bad",  "Grounding": "bad"},

    # ID 22 — correct refusal but adds opinionated list of what the app IS for (not in doc); tone is ok
    22: {"Fluency": "good", "Grammar": "good", "Tone": "ok",  "Length": "bad",  "Grounding": "ok"},

    # ID 23 — says "yes, use it for grocery budget" — doc has no such feature; out of scope
    23: {"Fluency": "good", "Grammar": "good", "Tone": "ok",  "Length": "bad",  "Grounding": "bad"},

    # ID 24 — correctly says it can't answer (weather is out of scope); good refusal
    24: {"Fluency": "good", "Grammar": "good", "Tone": "good", "Length": "good", "Grounding": "good"},
}
# fmt: on

LATENCY_THRESHOLDS = {"good": 15_000, "ok": 25_000}


def latency_rating(ms: float) -> str:
    if ms <= LATENCY_THRESHOLDS["good"]:
        return "good"
    if ms <= LATENCY_THRESHOLDS["ok"]:
        return "ok"
    return "bad"


def main() -> None:
    df = pd.read_excel("assignment_02.xlsx")

    # empty scoring columns were saved as float NaN; cast to object so strings fit
    score_cols = ["Fluency", "Grammar", "Tone", "Length", "Grounding", "Latency", "final_score"]
    df[score_cols] = df[score_cols].astype(object)

    for _, row in df.iterrows():
        rid = int(row["id"])
        scores = SCORES[rid].copy()
        scores["Latency"] = latency_rating(row["latency_ms"])
        scores["final_score"] = final_score(scores)

        for col, val in scores.items():
            df.loc[df["id"] == rid, col] = val

    df.to_excel("assignment_03.xlsx", index=False)

    pass_count = (df["final_score"] == "pass").sum()
    fail_count = (df["final_score"] == "fail").sum()
    print(f"Wrote assignment_03.xlsx — {pass_count} pass / {fail_count} fail")

    print("\nPer-row summary:")
    for _, row in df.iterrows():
        print(
            f"  [{int(row['id']):>2}] {row['final_score']:4}  "
            f"Fl={row['Fluency']:4} Gr={row['Grammar']:4} "
            f"To={row['Tone']:4} Le={row['Length']:4} "
            f"Gnd={row['Grounding']:4} Lat={row['Latency']:4}"
        )


if __name__ == "__main__":
    main()
