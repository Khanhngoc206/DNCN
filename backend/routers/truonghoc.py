from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from routers.auth import pwd

from database import get_db
import models
from models.truonghoc import TruongHoc
from schemas.truonghoc import TruongCreate, TruongResponse

router = APIRouter(prefix="/truonghoc", tags=["Trường học"])

# ================================================================
# 🟢 THÊM TRƯỜNG (không có username/password)
# ================================================================
@router.post("/", response_model=TruongResponse)
def create_truong(data: TruongCreate, db: Session = Depends(get_db)):
    obj = models.TruongHoc(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

# ================================================================
# 🟢 LẤY TẤT CẢ TRƯỜNG
# ================================================================
@router.get("/", response_model=list[TruongResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(models.TruongHoc).all()

# ================================================================
# 🟢 LẤY 1 TRƯỜNG
# ================================================================
@router.get("/{id}")
def get_one(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.TruongHoc).filter(models.TruongHoc.matruong == id).first()
    if not obj:
        raise HTTPException(404, "Không tìm thấy trường")

    return {
        "matruong": obj.matruong,
        "tentruong": obj.tentruong,
        "diachi": obj.diachi,
        "sodienthoai": obj.sodienthoai
    }

# ================================================================
# 🟢 XÓA TRƯỜNG
# ================================================================
@router.delete("/{id}")
def delete_truong(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.TruongHoc).filter(models.TruongHoc.matruong == id).first()
    if not obj:
        raise HTTPException(404, "Không tìm thấy trường")
    db.delete(obj)
    db.commit()
    return {"message": "Đã xóa"}

# ================================================================
# 🟢 CẬP NHẬT TRƯỜNG
# ================================================================
@router.put("/{id}")
def update_one(id: int, data: dict, db: Session = Depends(get_db)):
    obj = db.query(models.TruongHoc).filter(models.TruongHoc.matruong == id).first()

    if not obj:
        raise HTTPException(404, "Không tìm thấy trường")

    obj.tentruong = data.get("tentruong", obj.tentruong)
    obj.diachi = data.get("diachi", obj.diachi)
    obj.sodienthoai = data.get("sodienthoai", obj.sodienthoai)

    db.commit()
    db.refresh(obj)

    return {"message": "Cập nhật thành công"}

# ================================================================
# 🟢 ĐĂNG KÝ TRƯỜNG CÓ TÀI KHOẢN
# ================================================================
@router.post("/register", response_model=TruongResponse)
def create_school(data: TruongCreate, db: Session = Depends(get_db)):
    hashed = pwd.hash(data.password)

    new_school = TruongHoc(
        tentruong=data.tentruong,
        diachi=data.diachi,
        sodienthoai=data.sodienthoai,
        username=data.username,
        password_hash=hashed
    )

    db.add(new_school)
    db.commit()
    db.refresh(new_school)
    return new_school
