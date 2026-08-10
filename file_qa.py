import os
import sys

from openai import OpenAI

client = OpenAI(
    base_url="https://api.anthropic.com/v1/",
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

SYSTEM_PROMPT = (
    "You answer questions using ONLY the document provided below. Do not use "
    "any outside knowledge and do not guess. When you answer, quote the exact "
    "passage from the document that supports your answer. If the answer is not "
    "in the document, reply with exactly this sentence and nothing else: "
    "\"I can't find that in the document.\""
)


def main():
    if len(sys.argv) >= 3:
        file_path = sys.argv[1]
        question = sys.argv[2]
    else:
        file_path = input("File path: ")
        question = input("Question: ")

    with open(file_path, encoding="utf-8") as f:
        document = f.read()

    user_message = f"Document:\n{document}\n\nQuestion: {question}"

    response = client.chat.completions.create(
        model="claude-haiku-4-5",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
