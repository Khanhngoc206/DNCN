import pandas as pd
import random
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "size_data.csv")

rows = []

for _ in range(200):
    chieucao = random.randint(130, 180)
    cannang = random.randint(30, 85)
    gioitinh = random.choice([0, 1])  # 0=female, 1=male

    # logic size
    if chieucao < 150:
        size = "S"
    elif chieucao < 160:
        size = "M"
    elif chieucao < 170:
        size = "L"
    else:
        size = "XL"

    rows.append([chieucao, cannang, gioitinh, size])

df = pd.DataFrame(rows, columns=["chieucao", "cannang", "gioitinh", "size"])
df.to_csv(DATA_PATH, index=False)

print("✔ Tạo dataset thành công →", DATA_PATH)
