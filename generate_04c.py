"""Task 4 experiment C — temperature=0 (greedy) + 3 few-shot examples in prompt."""

import json
import time

import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

from scoring import CRITERIA

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
KNOWLEDGE_BASE_PATH = "family_task_guide.txt"
QUESTIONS_PATH = "data/questions.json"
OUTPUT_PATH = "assignment_04c.xlsx"
MAX_NEW_TOKENS = 80

# Change vs baseline: temperature=0 (greedy decoding) + 3 few-shot examples that
# each demonstrate grounded answers and one grounded refusal.
SYSTEM_PROMPT = (
    "You are a helpful assistant for the Kaplan family task-management system. "
    "Answer using ONLY the document below. Never add information that is not "
    "explicitly in the document. Answer in 1-3 sentences of plain prose.\n\n"
    "If the answer is not in the document reply with exactly: "
    "\"I can't find that in the document.\"\n\n"
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


def build_messages(document: str, question: str) -> list[dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT.format(document=document)},
        {"role": "user", "content": question},
    ]


def main() -> None:
    with open(KNOWLEDGE_BASE_PATH, encoding="utf-8") as f:
        document = f.read()

    with open(QUESTIONS_PATH, encoding="utf-8") as f:
        questions = json.load(f)

    print(f"Loading {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
    print("Loaded.")

    rows = []
    for item in questions:
        messages = build_messages(document, item["question"])
        text = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = tokenizer(text, return_tensors="pt")
        input_token_count = inputs["input_ids"].shape[1]

        start = time.perf_counter()
        # temperature=0 → greedy decoding, fully deterministic
        output = model.generate(
            **inputs, max_new_tokens=MAX_NEW_TOKENS, temperature=1e-9, do_sample=False
        )
        latency_ms = round((time.perf_counter() - start) * 1000)

        new_tokens = output[0][input_token_count:]
        output_token_count = len(new_tokens)
        generated = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

        print(f"[{item['id']:>2}] {latency_ms:>6} ms  {item['question'][:60]}")

        row = {
            "id": item["id"],
            "question": item["question"],
            "category": item["category"],
            "section": item["section"],
            "generated_description": generated,
            "latency_ms": latency_ms,
            "input_tokens": input_token_count,
            "output_tokens": output_token_count,
        }
        for criterion in CRITERIA:
            row[criterion] = ""
        row["final_score"] = ""
        rows.append(row)

    df = pd.DataFrame(rows)
    df.to_excel(OUTPUT_PATH, index=False)
    print(f"\nWrote {len(df)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
