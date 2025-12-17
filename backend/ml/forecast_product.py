import pickle
import os
import pandas as pd
from sqlalchemy.orm import Session

from backend import models

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


def get_sale_history(db: Session, masanpham: int):
    """
    Trả về dataframe:
    ds = ngày
    y = số lượng bán theo ngày (sẽ gom theo tháng)
    """

    data = db.query(
        models.CTDonHang.soluong,
        models.DonHang.ngaydat
    ).join(
        models.DonHang, models.DonHang.id == models.CTDonHang.madon
    ).join(
        models.SanPhamPhienBan,
        models.SanPhamPhienBan.id == models.CTDonHang.maphienban
    ).filter(
        models.SanPhamPhienBan.masanpham == masanpham
    ).all()

    if not data:
        return None

    df = pd.DataFrame(data, columns=["y", "ds"])

    df["ds"] = pd.to_datetime(df["ds"])

    # GOM THEO THÁNG
    df = df.groupby(pd.Grouper(key="ds", freq="M")).sum().reset_index()

    return df


def forecast_product(db: Session, masanpham: int, so_thang: int = 12):
    df = get_sale_history(db, masanpham)

    if df is None or df.empty:
        return None

    # load model
    model = load_model(masanpham)

    # nếu chưa train → train lần đầu
    if model is None:
        from prophet import Prophet
        model = Prophet()
        model.fit(df)

        save_path = os.path.join(MODEL_FOLDER, f"product_{masanpham}.pkl")
        with open(save_path, "wb") as f:
            pickle.dump(model, f)

    # Tạo tương lai
    future = model.make_future_dataframe(periods=so_thang, freq="M")
    result = model.predict(future)

    return result.tail(so_thang)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
