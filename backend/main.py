from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import (
    truonghoc,
    khoilop,
    sanpham,
    sanpham_phienban,
    size,
    donhang,
    chitiet_donhang,
    dudoan,
    forecast,
    forecast_product,
    auth,
    thongke,
    ai_predict_size,
    donhang_khachle
)

# =====================================
# ⚠️ KHÔNG TẠO BẢNG KHI DEPLOY
# (chỉ dùng khi DEV local)
# =====================================
# Base.metadata.create_all(bind=engine)

# =====================================
# FASTAPI APP
# =====================================
app = FastAPI(title="API Quản lý đồng phục học sinh")

# =====================================
# ✅ CORS – CHO LOCAL + DEPLOY
# =====================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # LOCAL
        "http://127.0.0.1:8001",
        "http://localhost:8001",

        # DEPLOY DJANGO (RENDER)
        "https://uniform-web.onrender.com",

        # hoặc tạm thời cho tất cả (khuyến nghị lúc test)
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# ROUTERS
# =====================================
app.include_router(auth.router)

app.include_router(truonghoc.router)
app.include_router(khoilop.router)

app.include_router(sanpham.router)
app.include_router(sanpham_phienban.router)
app.include_router(size.router)

app.include_router(donhang.router)
app.include_router(donhang_khachle.router)
app.include_router(chitiet_donhang.router)

app.include_router(dudoan.router)
app.include_router(forecast.router)
app.include_router(forecast_product.router)

app.include_router(ai_predict_size.router)
app.include_router(thongke.router, prefix="/thongke", tags=["Thống kê"])
