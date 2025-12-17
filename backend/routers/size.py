from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
from schemas.size import SizeCreate, SizeResponse

router = APIRouter(prefix="/size", tags=["Size – Tồn kho"])


# 1) Tạo size
@router.post("/", response_model=SizeResponse)
def create_size(data: SizeCreate, db: Session = Depends(get_db)):
    obj = models.SizePhienBan(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# 2) Lấy tất cả size
@router.get("/", response_model=list[SizeResponse])
def get_all_sizes(db: Session = Depends(get_db)):
    data = db.query(models.SizePhienBan).all()
    return data

@router.delete("/{id}")
def delete_size(id: int, db: Session = Depends(get_db)):
    obj = db.query(models.SizePhienBan).filter(models.SizePhienBan.id == id).first()

    if not obj:
        raise HTTPException(404, "Size không tồn tại")

    db.delete(obj)
    db.commit()
    return {"message": "Đã xóa size"}

@router.put("/{id}")
def update_size(id: int, data: SizeCreate, db: Session = Depends(get_db)):
    obj = db.query(models.SizePhienBan).filter(models.SizePhienBan.id == id).first()

    if not obj:
        raise HTTPException(404, "Size không tồn tại")

    obj.maphienban = data.maphienban
    obj.tensize = data.tensize
    obj.soluongton = data.soluongton

    db.commit()
    return obj
