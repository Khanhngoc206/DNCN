from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from database import get_db
from models.donhang import DonHang
from models.chitiet_donhang import ChiTietDonHang
from models.phienban import SanPhamPhienBan
from models.sanpham import SanPham  # 🔥 nhớ import đúng bảng sản phẩm

router = APIRouter(tags=["Thống kê"])


# ==========================
# 1. DOANH THU THEO NGÀY
# ==========================
@router.get("/revenue")
def revenue_chart(db: Session = Depends(get_db)):
    rows = db.query(
        DonHang.ngaydat,
        DonHang.tongtien
    ).all()

    labels = []
    values = []

    for ngay, tong in rows:
        labels.append(str(ngay))
        # Nếu tongtien = None thì thay bằng 0
        values.append(float(tong) if tong is not None else 0)

    return {"labels": labels, "values": values}


# ==========================
# 2. THỐNG KÊ SIZE
# ==========================
@router.get("/size")
def size_stat(db: Session = Depends(get_db)):
    rows = db.query(
        ChiTietDonHang.tensize,
        func.sum(ChiTietDonHang.soluong)
    ).group_by(
        ChiTietDonHang.tensize
    ).all()

    labels = []
    values = []

    for size, total in rows:
        size_label = size if size else "Không chọn"
        labels.append(size_label)
        values.append(int(total))

    return {"labels": labels, "values": values}


# ==========================
# 3. TỔNG DOANH THU
# ==========================
@router.get("/tong_doanh_thu")
def tong_doanh_thu(db: Session = Depends(get_db)):
    total = db.query(func.sum(DonHang.tongtien)).scalar() or 0
    return {"total": float(total)}


# ==========================
# 4. TỔNG ĐƠN HÀNG
# ==========================
@router.get("/tong_don_hang")
def tong_don_hang(db: Session = Depends(get_db)):
    return {"total": db.query(DonHang).count()}


# ==========================
# 5. SIZE BÁN CHẠY NHẤT
# ==========================
@router.get("/size_max")
def size_max(db: Session = Depends(get_db)):
    row = db.query(
        ChiTietDonHang.tensize,
        func.sum(ChiTietDonHang.soluong).label("sl")
    ).group_by(
        ChiTietDonHang.tensize
    ).order_by(
        desc("sl")
    ).first()

    if not row:
        return {"size": "-"}

    return {"size": row[0]}


# ==========================
# 6. SẢN PHẨM BÁN CHẠY NHẤT
# ==========================
@router.get("/best_product")
def best_product(db: Session = Depends(get_db)):
    row = db.query(
        SanPhamPhienBan.masanpham,
        func.sum(ChiTietDonHang.soluong).label("sl")
    ).join(
        ChiTietDonHang,
        ChiTietDonHang.maphienban == SanPhamPhienBan.maphienban
    ).group_by(
        SanPhamPhienBan.masanpham
    ).order_by(
        desc("sl")
    ).first()

    if not row:
        return {"sanpham": "-"}

    return {"sanpham": f"Sản phẩm #{row[0]}", "soluong": int(row[1])}

