import pickle
import os
import pandas as pd
from sqlalchemy.orm import Session

import models

MODEL_FOLDER = os.path.dirname(__file__)

def train_model_for_product(df: pd.DataFrame, product_id: int):
    from prophet import Prophet

    model = Prophet()

    model.fit(df)

    save_path = os.path.join(MODEL_FOLDER, f"product_{product_id}.pkl")
    with open(save_path, "wb") as f:
        pickle.dump(model, f)

    return save_path


def load_model(product_id: int):
    path = os.path.join(MODEL_FOLDER, f"product_{product_id}.pkl")
    if not os.path.exists(path):
        return None

    with open(path, "rb") as f:
        return pickle.load(f)


def get_sale_history(db, masanpham):
    query = (
        db.query(
            models.ChiTietDonHang.soluong,
            models.DonHang.created_at
        )
        .join(
            models.DonHang,
            models.ChiTietDonHang.madonhang == models.DonHang.madonhang
        )
        .filter(models.ChiTietDonHang.masanpham == masanpham)
    )

    return query.all()
