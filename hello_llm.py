import json
import os

from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(
    base_url="https://api.anthropic.com/v1/",
    api_key=os.environ["ANTHROPIC_API_KEY"],
)


def ask(user, system=None, temperature=None, model="claude-haiku-4-5"):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": user})

    kwargs = {"model": model, "messages": messages}
    if temperature is not None:
        kwargs["temperature"] = temperature

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


# --- Exercise 1: plain hello ---
print("=== Exercise 1: plain hello ===")
print(ask("Say hello in one sentence."))


# --- Exercise 1b: system prompt ---
print("\n=== 1b: system prompt (pirate persona) ===")
print(ask("Say hello in one sentence.", system="You are a pirate. Answer in one sentence."))


# --- Exercise 1b: temperature ---
print("\n=== 1b: temperature=0, twice (should be ~identical) ===")
print(ask("Say hello in one sentence.", temperature=0))
print(ask("Say hello in one sentence.", temperature=0))

print("\n=== 1b: temperature=1, twice (should vary) ===")
print(ask("Say hello in one sentence.", temperature=1))
print(ask("Say hello in one sentence.", temperature=1))


# --- Exercise 1b: structured output, two ways ---
print("\n=== 1b: structured output ===")
json_system = (
    "Reply with JSON only, no other text before or after. Do not use markdown "
    "code fences or any other formatting -- output raw JSON text only, starting "
    "with { and ending with }. The JSON object must have exactly two fields: "
    "answer (a string) and confidence (a number between 0 and 1)."
)
raw_reply = ask("Say hello in one sentence.", system=json_system)
print("raw reply:", raw_reply)


def strip_code_fence(text):
    # models sometimes ignore "no markdown" and wrap the reply in ```json ... ```
    # anyway -- a defensive strip like this is standard practice, not a workaround
    # for a one-off bug, since you can't fully rely on the prompt alone
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        if text.endswith("```"):
            text = text.rsplit("```", 1)[0]
    return text.strip()


raw_reply = strip_code_fence(raw_reply)

print("--- (a) parsed with the json module ---")
data = json.loads(raw_reply)
print("answer:", data["answer"])
print("confidence:", data["confidence"])


class Answer(BaseModel):
    answer: str
    confidence: float


print("--- (b) parsed with pydantic ---")
parsed = Answer.model_validate_json(raw_reply)
print("answer:", parsed.answer)
print("confidence:", parsed.confidence)
