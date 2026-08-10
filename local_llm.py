from transformers import pipeline

generator = pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")

prompt = "Give me a recepie for pizza without gluten."
result = generator(prompt, max_new_tokens=200)

print(result[0]["generated_text"])
