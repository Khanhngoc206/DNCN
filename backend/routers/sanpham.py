from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.sanpham import SanPham
from models.phienban import SanPhamPhienBan
from models.size import SizePhienBan
from schemas.sanpham import (
    SanPhamCreate,
    SanPhamUpdate,
    SanPhamResponse
)

router = APIRouter(prefix="/sanpham", tags=["Sản phẩm"])

# ============================================================
# 1. LẤY TẤT CẢ SẢN PHẨM
# ============================================================
@router.get("/", response_model=list[SanPhamResponse])
def get_all_sanpham(db: Session = Depends(get_db)):
    return db.query(SanPham).order_by(SanPham.masanpham).all()


# ============================================================
# 2. LẤY SẢN PHẨM THEO ID
# ============================================================
@router.get("/{id}", response_model=SanPhamResponse)
def get_sanpham(id: int, db: Session = Depends(get_db)):
    sp = db.query(SanPham).filter(
        SanPham.masanpham == id
    ).first()

    if not sp:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    return sp


# ============================================================
# 3. LẤY DANH SÁCH SIZE THEO SẢN PHẨM (PHIÊN BẢN)
# ============================================================
@router.get("/phienban/{masanpham}")
def get_phienban(masanpham: int, db: Session = Depends(get_db)):

    # 🔹 Lấy sản phẩm để lấy giá bán
    sanpham = db.query(SanPham).filter(
        SanPham.masanpham == masanpham
    ).first()

    if not sanpham:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    # 🔹 JOIN sanpham_phienban → size_phienban
    rows = (
        db.query(SanPhamPhienBan, SizePhienBan)
        .join(
            SizePhienBan,
            SanPhamPhienBan.maphienban == SizePhienBan.maphienban
        )
        .filter(SanPhamPhienBan.masanpham == masanpham)
        .all()
    )

    if not rows:
        return []

    return [
        {
            "maphienban": pb.maphienban,
            "masize": sz.masize,
            "size": sz.tensize,                  # ✅ size đúng bảng
            "dongia": float(sanpham.giaban)      # ✅ giá từ bảng sanpham
        }
        for pb, sz in rows
    ]


# ============================================================
# 4. THÊM SẢN PHẨM MỚI
# ============================================================
@router.post("/", response_model=SanPhamResponse)
def create_sanpham(data: SanPhamCreate, db: Session = Depends(get_db)):

    new_sp = SanPham(
        tensanpham=data.tensanpham,
        danhmuc=data.danhmuc,
        giaban=data.giaban,
        mota=data.mota,
        hinhanh=data.hinhanh
    )

    db.add(new_sp)
    db.commit()
    db.refresh(new_sp)

    return new_sp


# ============================================================
# 5. CẬP NHẬT SẢN PHẨM
# ============================================================
@router.put("/{id}", response_model=SanPhamResponse)
def update_sanpham(
    id: int,
    data: SanPhamUpdate,
    db: Session = Depends(get_db)
):
    sp = db.query(SanPham).filter(
        SanPham.masanpham == id
    ).first()

    if not sp:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(sp, field, value)

    db.commit()
    db.refresh(sp)

    return sp


# ============================================================
# 6. XOÁ SẢN PHẨM
# ============================================================
@router.delete("/{id}")
def delete_sanpham(id: int, db: Session = Depends(get_db)):

    sp = db.query(SanPham).filter(
        SanPham.masanpham == id
    ).first()

    if not sp:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")

    db.delete(sp)
    db.commit()

    return {"message": "Đã xóa sản phẩm"}
