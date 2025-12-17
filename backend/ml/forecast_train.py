import pandas as pd
from prophet import Prophet
import pickle

# ================================
# 1. TẠO DATA DOANH THU MẪU
# ================================
# ds = ngày, y = doanh thu / số lượng bán
data = {
    "ds": pd.date_range(start="2020-01-01", periods=48, freq="M"),
    "y": [
        120,130,150,160,180,200,220,210,190,170,160,150,
        130,140,155,165,195,215,230,240,210,180,175,165,
        150,160,170,180,200,230,250,260,240,220,210,205,
        180,185,190,210,230,260,280,300,320,310,305,290
    ]
}

df = pd.DataFrame(data)

# ================================
# 2. TRAIN MÔ HÌNH PROPHET
# ================================
model = Prophet()
model.fit(df)

# ================================
# 3. LƯU FILE MÔ HÌNH
# ================================
with open("forecast_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✔ Đã train xong mô hình Prophet và lưu forecast_model.pkl")
