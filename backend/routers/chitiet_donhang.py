from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from backend import models
from schemas.chitiet_donhang import CTDonHangCreate, CTDonHangResponse

router = APIRouter(prefix="/ctdonhang", tags=["Chi tiết đơn hàng"])

@router.get("/{madon}", response_model=list[CTDonHangResponse])
def get_by_order(madon: int, db: Session = Depends(get_db)):
    ds = db.query(models.CTDonHang).filter(models.CTDonHang.madon == madon).all()
    return ds

@router.post("/", response_model=CTDonHangResponse)
def create(data: CTDonHangCreate, db: Session = Depends(get_db)):
    obj = models.CTDonHang(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return 

@router.delete("/{id}")
def delete_ct(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.CTDonHang).filter(models.CTDonHang.id == id).first()
    if not obj:
        raise HTTPException(404, "Chi tiết không tồn tại")

    db.delete(obj)
    db.commit()
    return {"message": "Đã xóa mục chi tiết"}
