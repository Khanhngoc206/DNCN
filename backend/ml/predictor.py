import pickle
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(MODEL_PATH, "rb") as f:
    model, size_map = pickle.load(f)

reverse_map = {v: k for k, v in size_map.items()}

def predict_size(chieucao, cannang, gioitinh):
    X = np.array([[chieucao, cannang, gioitinh]])
    pred_num = model.predict(X)[0]
    return reverse_map[pred_num]
