from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from backend import models
from schemas.khoilop import KhoiLopCreate, KhoiLopResponse

router = APIRouter(prefix="/khoilop", tags=["Khối lớp"])

# --------------------------
# Tạo khối lớp
# --------------------------
@router.post("/", response_model=KhoiLopResponse)
def create_khoi(data: KhoiLopCreate, db: Session = Depends(get_db)):
    obj = models.KhoiLop(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# --------------------------
# Lấy tất cả khối lớp
# --------------------------
@router.get("/", response_model=list[KhoiLopResponse])
def get_all_khoi(db: Session = Depends(get_db)):
    return db.query(models.KhoiLop).all()


# --------------------------
# Lấy 1 khối lớp theo makhoi
# --------------------------
@router.get("/{makhoi}", response_model=KhoiLopResponse)
def get_one_khoi(makhoi: int, db: Session = Depends(get_db)):
    obj = db.query(models.KhoiLop).filter(models.KhoiLop.makhoi == makhoi).first()

    if not obj:
        raise HTTPException(status_code=404, detail="Khối lớp không tồn tại")

    return obj
