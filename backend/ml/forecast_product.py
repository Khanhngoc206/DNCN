import pickle
import os
import pandas as pd
from sqlalchemy.orm import Session
from prophet import Prophet

import models

MODEL_FOLDER = os.path.dirname(__file__)

# =========================================================
# LOAD / TRAIN MODEL
# =========================================================

def train_model_for_product(df: pd.DataFrame, product_id: int):
    model = Prophet()
    model.fit(df)

    save_path = os.path.join(MODEL_FOLDER, f"product_{product_id}.pkl")
    with open(save_path, "wb") as f:
        pickle.dump(model, f)

    return model


def load_model(product_id: int):
    path = os.path.join(MODEL_FOLDER, f"product_{product_id}.pkl")
    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return pickle.load(f)


# =========================================================
# GET SALE HISTORY
# =========================================================

def get_sale_history(db: Session, masanpham: int):
    rows = (
        db.query(
            models.DonHang.created_at,
            models.ChiTietDonHang.soluong,
        )
        .join(
            models.DonHang,
            models.ChiTietDonHang.madonhang == models.DonHang.madonhang
        )
        .filter(models.ChiTietDonHang.masanpham == masanpham)
        .all()
    )

    if not rows:
        return None

    df = pd.DataFrame(rows, columns=["ds", "y"])
    df = df.groupby("ds").sum().reset_index()

    return df


# =========================================================
# ⭐ HÀM BỊ THIẾU → GÂY CRASH
# =========================================================

def forecast_product(db: Session, masanpham: int, so_thang: int):
    df = get_sale_history(db, masanpham)
    if df is None or df.empty:
        return None

    model = load_model(masanpham)
    if model is None:
        model = train_model_for_product(df, masanpham)

    future = model.make_future_dataframe(periods=so_thang, freq="M")
    forecast = model.predict(future)

    result = forecast[["ds", "yhat"]].tail(so_thang)
    result["thang"] = result["ds"].dt.strftime("%Y-%m")
    result["S"] = result["yhat"].clip(lower=0).round().astype(int)
    result["M"] = result["S"]
    result["L"] = result["S"]
    result["XL"] = result["S"]

    return result
