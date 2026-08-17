"""Task 2 -- generate an answer for every question with a deliberately small
local model (Qwen2.5-0.5B-Instruct), recording latency and token counts
alongside each output. Writes assignment_02.xlsx with blank columns for the
human (Task 3) and judge (Task 6) scoring passes.
"""

import json
import time

import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

from scoring import CRITERIA

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
KNOWLEDGE_BASE_PATH = "family_task_guide.txt"
QUESTIONS_PATH = "data/questions.json"
OUTPUT_PATH = "assignment_02.xlsx"
MAX_NEW_TOKENS = 200

# The rubric (RUBRIC.md) is the spec for this prompt: grounded-only,
# 1-3 sentences, warm household-assistant tone, exact refusal sentence when
# the answer isn't in the document, no lists.
SYSTEM_PROMPT = (
    "You are a warm, helpful assistant for the Kaplan family's shared "
    "task-management system. Answer the family member's question using "
    "ONLY the document below as your source of facts about the system -- "
    "do not use outside knowledge and do not invent policies, features, or "
    "rules that are not stated in the document.\n\n"
    "Format: answer in 1 to 3 sentences of plain prose. Do not use bullet "
    "points or numbered lists. Sound like a helpful person talking to a "
    "family member, not a salesperson or a legal notice.\n\n"
    "If the document does not contain the answer, reply with exactly this "
    "sentence and nothing else: \"I can't find that in the document.\"\n\n"
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
        output = model.generate(**inputs, max_new_tokens=MAX_NEW_TOKENS)
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
