import pandas as pd

for f in ["assignment_04a.xlsx", "assignment_04b.xlsx", "assignment_04c.xlsx"]:
    df = pd.read_excel(f)
    label = f.replace("assignment_", "").replace(".xlsx", "").upper()
    print(f"\n=== {label} ===")
    for _, r in df.iterrows():
        print(f"[{int(r['id']):>2}] Q: {r['question'][:55]}")
        print(f"      A: {str(r['generated_description'])[:200]}")
        print(f"      lat={r['latency_ms']}ms")
