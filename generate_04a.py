"""Task 4 experiment A — stricter grounding prompt + one-shot example + shorter output."""

import json
import time

import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer

from scoring import CRITERIA

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"
KNOWLEDGE_BASE_PATH = "family_task_guide.txt"
QUESTIONS_PATH = "data/questions.json"
OUTPUT_PATH = "assignment_04a.xlsx"
MAX_NEW_TOKENS = 80  # shorter = faster and fewer hallucinated sentences

# Change vs baseline: added explicit "do not infer or extrapolate" warning and
# one concrete few-shot example showing grounded refusal and grounded answer.
SYSTEM_PROMPT = (
    "You are a helpful assistant for the Kaplan family task-management system. "
    "Answer the family member's question using ONLY the exact information in the "
    "document below. Do not infer, extrapolate, or add any information that is not "
    "explicitly stated in the document — even if the addition seems helpful or "
    "obvious.\n\n"
    "Format: answer in 1 to 3 sentences of plain prose. No bullet points or lists.\n\n"
    "If the document does not contain the answer, reply with exactly this sentence "
    "and nothing else: \"I can't find that in the document.\"\n\n"
    "Example:\n"
    "Question: Can two people be responsible for the same task?\n"
    "Answer: No — tasks can only be assigned to exactly one person at a time; "
    "if two people need to work on something together, it should be split into "
    "two separate tasks.\n\n"
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
