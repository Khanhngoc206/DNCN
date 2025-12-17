from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date

from database import get_db
from models.donhang import DonHang
from models.chitiet_donhang import ChiTietDonHang

router = APIRouter(prefix="/donhang_khachle", tags=["Khách lẻ"])


class DonHangLe(BaseModel):
    hoten: str
    sdt: str
    diachi: str
    cart: dict   # { "1_M": {soluong:1, giaban:90000} }

@router.post("/dat_hang_khachle")
def dat_hang_khachle(data: dict, db: Session = Depends(get_db)):

    tongtien = sum(
        item["dongia"] * item["soluong"]
        for item in data["cart"].values()
    )

    dh = DonHang(
        tenkhach=data["tenkhach"],
        sodienthoai=data["sodienthoai"],
        diachi=data["diachi"],
        tongtien=tongtien
    )

    db.add(dh)
    db.flush()  # 🔥 LẤY madon

    for item in data["cart"].values():
        ct = ChiTietDonHang(
            madon=dh.madon,
            maphienban=item["maphienban"],
            tensize=item["size"],
            soluong=item["soluong"],
            dongia=item["dongia"]
        )
        db.add(ct)

    db.commit()

    return {"message": "Đặt hàng khách lẻ thành công"}