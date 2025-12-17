from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.donhang import DonHang
from models.chitiet_donhang import ChiTietDonHang
from schemas.donhang import DonHangCreate
from backend import models
from datetime import date

router = APIRouter(prefix="/donhang", tags=["Đơn hàng"])


# ============================================================
# 1) LẤY DANH SÁCH ĐƠN HÀNG
# ============================================================
@router.get("/")
def get_all(db: Session = Depends(get_db)):

    ds = db.query(DonHang).order_by(models.DonHang.madon).all()

    return [
        {
            "madon": d.madon,
            "makh": d.makh,
            "matruong": d.matruong,
            "ngay": d.ngaydat or "",
            "tongtien": float(d.tongtien or 0),
            "trangthai": d.trangthai
        }
        for d in ds
    ]


# ============================================================
# 2) SỐ ĐƠN HÀNG CỦA TRƯỜNG
# ============================================================
@router.get("/school/{matruong}")
def don_hang_cua_truong(mattruong: int, db: Session = Depends(get_db)):
    ds = db.query(DonHang).filter(DonHang.matruong == mattruong).all()
    return [
        {
            "madon": d.madon,
            "ngay": d.ngaydat or "",
            "tongtien": float(d.tongtien or 0),
            "trangthai": d.trangthai
        }
        for d in ds
    ]


# ============================================================
# 3) TẠO ĐƠN HÀNG CHO TRƯỜNG
# ============================================================
@router.post("/dat_hang_truong")
def dat_hang_truong(data: dict, db: Session = Depends(get_db)):

    # 1. Tạo đơn hàng
    dh = DonHang(
        matruong=data["matruong"],   # ✅ phân biệt đơn trường
        tongtien=sum(
            item["dongia"] * item["soluong"]
            for item in data["cart"].values()
        )
    )
    db.add(dh)
    db.commit()
    db.refresh(dh)

    # 2. Chi tiết đơn hàng
    for item in data["cart"].values():
        ct = ChiTietDonHang(
            madon=dh.madon,
            makhoi=data["matruong"],          # ✅ THEO DB (bạn đang dùng)
            maphienban=item["maphienban"],
            tensize=item["tensize"],
            soluong=item["soluong"],
            dongia=item["dongia"]
        )
        db.add(ct)

    db.commit()

    return {"success": True}


# ============================================================
# 4) TẠO ĐƠN HÀNG KHÁCH LẺ
# ============================================================
@router.post("/")
def create_order(data: DonHangCreate, db: Session = Depends(get_db)):

    if data.is_school:
        dh = DonHang(
            matruong=data.matruong,
            ngaydat=date.today(),
            trangthai="Chờ duyệt"
        )
    else:
        dh = DonHang(
            hoten=data.hoten,
            sdt=data.sdt,
            diachi=data.diachi,
            ngaydat=date.today(),
            trangthai="Chờ duyệt"
        )

    db.add(dh)
    db.commit()
    db.refresh(dh)

    tong = 0
    for masp, item in data.cart.items():

        key = str(masp)
        parts = key.split("_")
        masanpham = int(parts[0])
        size = parts[1] if len(parts) > 1 else item.get("size")

        ct = ChiTietDonHang(
            madon=dh.madon,
            masanpham=masanpham,
            masize=size,
            soluong=item["soluong"],
            dongia=item["giaban"],                # ⭐ CHUẨN HOÁ GIÁ
            thanhtien=item["giaban"] * item["soluong"]
        )
        tong += ct.thanhtien
        db.add(ct)

    dh.tongtien = tong
    db.commit()

    return {"message": "Tạo đơn thành công", "madon": dh.madon}


# ============================================================
# 5) CẬP NHẬT TRẠNG THÁI
# ============================================================
@router.put("/{id}/status")
def update_status(id: int, data: dict, db: Session = Depends(get_db)):
    dh = db.query(DonHang).filter(DonHang.madon == id).first()
    if not dh:
        raise HTTPException(404, "Không tìm thấy đơn hàng")

    dh.trangthai = data["trangthai"]
    db.commit()
    return {"message": "Cập nhật thành công"}


# ============================================================
# 6) XÓA ĐƠN HÀNG
# ============================================================
@router.delete("/{id}")
def delete_order(id: int, db: Session = Depends(get_db)):
    dh = db.query(DonHang).filter(DonHang.madon == id).first()
    if not dh:
        raise HTTPException(404, "Đơn hàng không tồn tại")

    db.delete(dh)
    db.commit()
    return {"message": "Đã xóa đơn hàng"}


# ============================================================
# 7) LẤY CHI TIẾT ĐƠN HÀNG
# ============================================================
@router.get("/{id}")
def get_order_detail(id: int, db: Session = Depends(get_db)):
    dh = db.query(DonHang).filter(DonHang.madon == id).first()
    if not dh:
        raise HTTPException(404, "Không tìm thấy đơn hàng")

    items = db.query(ChiTietDonHang).filter(ChiTietDonHang.madon == id).all()

    return {
        "madon": dh.madon,
        "makh": dh.makh,
        "matruong": dh.matruong,
        "ngay": dh.ngaydat,
        "tongtien": float(dh.tongtien or 0),
        "trangthai": dh.trangthai,
        "items": [
            {
                "masanpham": c.masanpham,
                "masize": c.masize,
                "soluong": c.soluong,
                "dongia": float(c.dongia),
                "thanhtien": float(c.thanhtien)
            }
            for c in items
        ]
    }
