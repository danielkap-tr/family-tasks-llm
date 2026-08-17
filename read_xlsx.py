import pandas as pd
df = pd.read_excel("assignment_02.xlsx")
print(df.columns.tolist())
for _, r in df.iterrows():
    print(f"--- ID {int(r['id'])} ---")
    print("Q:", r["question"])
    print("A:", r["generated_description"])
    print(f"latency: {r['latency_ms']}ms")
    print()
