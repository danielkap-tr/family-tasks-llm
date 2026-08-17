"""Task 4 — run all three prompt experiments using Claude (Anthropic API).

Replaces the local Qwen runner which requires too much RAM on this machine.
Each experiment uses the same Claude model; only the system prompt and
max_tokens differ, matching the intent of generate_04a/b/c.py exactly.
"""

import json
import os
import time

import pandas as pd
from anthropic import Anthropic

from scoring import CRITERIA

KNOWLEDGE_BASE_PATH = "family_task_guide.txt"
QUESTIONS_PATH = "data/questions.json"
MODEL = "claude-haiku-4-5"

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── Experiment definitions ───────────────────────────────────────────────────

# Experiment A: stricter grounding instruction + one-shot example, 80 max tokens
PROMPT_A = (
    "You are a helpful assistant for the Kaplan family task-management system. "
    "Answer the family member's question using ONLY the exact information in the "
    "document below. Do not infer, extrapolate, or add any information that is not "
    "explicitly stated in the document — even if the addition seems helpful or "
    "obvious.\n\n"
    "Format: answer in 1 to 3 sentences of plain prose. No bullet points or lists.\n\n"
    'If the document does not contain the answer, reply with exactly this sentence '
    'and nothing else: "I can\'t find that in the document."\n\n'
    "Example:\n"
    "Question: Can two people be responsible for the same task?\n"
    "Answer: No — tasks can only be assigned to exactly one person at a time; "
    "if two people need to work on something together, it should be split into "
    "two separate tasks.\n\n"
    "Document:\n{document}"
)

# Experiment B: baseline prompt, very short max_tokens (forces brevity)
PROMPT_B = (
    "You are a warm, helpful assistant for the Kaplan family's shared "
    "task-management system. Answer the family member's question using "
    "ONLY the document below as your source of facts about the system -- "
    "do not use outside knowledge and do not invent policies, features, or "
    "rules that are not stated in the document.\n\n"
    "Format: answer in 1 to 3 sentences of plain prose. Do not use bullet "
    "points or numbered lists. Sound like a helpful person talking to a "
    "family member, not a salesperson or a legal notice.\n\n"
    'If the document does not contain the answer, reply with exactly this '
    'sentence and nothing else: "I can\'t find that in the document."\n\n'
    "Document:\n{document}"
)

# Experiment C: three few-shot examples demonstrating grounded answers
PROMPT_C = (
    "You are a helpful assistant for the Kaplan family task-management system. "
    "Answer using ONLY the document below. Never add information that is not "
    "explicitly in the document. Answer in 1-3 sentences of plain prose.\n\n"
    'If the answer is not in the document reply with exactly: '
    '"I can\'t find that in the document."\n\n'
    "Examples:\n"
    "Q: Does someone need to be an admin to create a task?\n"
    "A: No, any registered family member can create a task — there is no admin role.\n\n"
    "Q: Can a task be assigned to two people at once?\n"
    "A: No, each task must have exactly one responsible person; "
    "if two people need to share the work, the task should be split into two.\n\n"
    "Q: What is the default reminder?\n"
    "A: The default reminder is sent the evening before the due date.\n\n"
    "Document:\n{document}"
)

EXPERIMENTS = [
    {"name": "A", "output": "assignment_04a.xlsx", "prompt": PROMPT_A, "max_tokens": 120},
    {"name": "B", "output": "assignment_04b.xlsx", "prompt": PROMPT_B, "max_tokens": 80},
    {"name": "C", "output": "assignment_04c.xlsx", "prompt": PROMPT_C, "max_tokens": 120},
]


def run_experiment(exp: dict, document: str, questions: list) -> None:
    print(f"\n=== Experiment {exp['name']} → {exp['output']} ===")
    rows = []
    for item in questions:
        system = exp["prompt"].format(document=document)
        start = time.perf_counter()
        response = client.messages.create(
            model=MODEL,
            max_tokens=exp["max_tokens"],
            system=system,
            messages=[{"role": "user", "content": item["question"]}],
        )
        latency_ms = round((time.perf_counter() - start) * 1000)
        generated = response.content[0].text.strip()
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens

        print(f"  [{item['id']:>2}] {latency_ms:>5} ms  {item['question'][:55]}")

        row = {
            "id": item["id"],
            "question": item["question"],
            "category": item["category"],
            "section": item["section"],
            "generated_description": generated,
            "latency_ms": latency_ms,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        }
        for criterion in CRITERIA:
            row[criterion] = ""
        row["final_score"] = ""
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(exp["output"], index=False)
    print(f"  Wrote {len(df)} rows to {exp['output']}")


def main() -> None:
    with open(KNOWLEDGE_BASE_PATH, encoding="utf-8") as f:
        document = f.read()
    with open(QUESTIONS_PATH, encoding="utf-8") as f:
        questions = json.load(f)

    for exp in EXPERIMENTS:
        run_experiment(exp, document, questions)

    print("\nAll experiments done.")


if __name__ == "__main__":
    main()
