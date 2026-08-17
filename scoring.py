"""Shared pass/fail rules from RUBRIC.md, applied identically by the human
scorer (Task 3), the improvement experiments (Task 4), and the judge (Task 6).
"""

CRITERIA = ["Fluency", "Grammar", "Tone", "Length", "Grounding", "Latency"]
NON_GROUNDING_CRITERIA = ["Fluency", "Grammar", "Tone", "Length", "Latency"]


def final_score(ratings: dict[str, str]) -> str:
    """ratings: dict mapping each of CRITERIA to 'good' | 'ok' | 'bad'.

    Go/no-go: Grounding not good -> automatic fail.
    Otherwise: pass requires >=4 of the other 5 criteria 'good' and 0 'bad'.
    """
    if ratings.get("Grounding") != "good":
        return "fail"

    values = [ratings.get(c) for c in NON_GROUNDING_CRITERIA]
    good_count = sum(1 for v in values if v == "good")
    bad_count = sum(1 for v in values if v == "bad")

    return "pass" if (good_count >= 4 and bad_count == 0) else "fail"
