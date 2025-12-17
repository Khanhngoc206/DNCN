import pickle
import os
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "forecast_model.pkl")

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

def du_bao_nam(so_thang: int = 12):
    # Tạo dataframe tương lai
    future = model.make_future_dataframe(periods=so_thang, freq="M")

    # Dự báo
    result = model.predict(future)

    # Trả về đúng số tháng cần thiết
    return result[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(so_thang)
