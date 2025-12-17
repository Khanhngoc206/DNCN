import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "size_data.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

df = pd.read_csv(DATA_PATH)

x = df[["chieucao", "cannang", "gioitinh"]]
y = df["size"]

model = DecisionTreeClassifier()
model.fit(x, y)

with open(MODEL_PATH, "wb") as f:
    pickle.dump(model, f)

print("✔ Train mô hình thành công")
print("✔ model.pkl đã được lưu tại:", MODEL_PATH)
