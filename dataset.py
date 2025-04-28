import os
import pandas as pd

data = []

for i in range(1, 379):
    try:
        with open(f"data/text_catehism/{i}.txt", encoding="utf-8") as f:
            cyrillic_text = f.read().strip()
        with open(f"data/transliterated_catehism/{i}.txt", encoding="utf-8") as f:
            latin_text = f.read().strip()

        if cyrillic_text and latin_text:
            data.append({"input_text": cyrillic_text, "target_text": latin_text})
    except Exception as e:
        continue

df = pd.DataFrame(data)
df.to_csv("data/dataset.csv", index=False)
