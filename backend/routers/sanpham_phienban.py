from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.phienban import SanPhamPhienBan
from backend.schemas.phienban import PhienBanCreate, PhienBanResponse

router = APIRouter(prefix="/phienban", tags=["Phiên bản sản phẩm"])

@router.post("/", response_model=PhienBanResponse)
def create(data: PhienBanCreate, db: Session = Depends(get_db)):
    obj = SanPhamPhienBan(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/", response_model=list[PhienBanResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(SanPhamPhienBan).all()


@router.get("/{id}", response_model=PhienBanResponse)
def get_one(id: int, db: Session = Depends(get_db)):
    obj = db.query(SanPhamPhienBan).filter(SanPhamPhienBan.maphienban == id).first()
    if not obj:
        raise HTTPException(404, "Không tìm thấy phiên bản sản phẩm")
    return obj


@router.delete("/{id}")
def delete_phienban(id: int, db: Session = Depends(get_db)):
    obj = db.query(SanPhamPhienBan).filter(SanPhamPhienBan.maphienban == id).first()
    if not obj:
        raise HTTPException(404, "Không tìm thấy phiên bản")

    db.delete(obj)
    db.commit()
    return {"message": "Đã xóa phiên bản"}


@router.put("/{id}", response_model=PhienBanResponse)
def update_phienban(id: int, data: PhienBanCreate, db: Session = Depends(get_db)):
    obj = db.query(SanPhamPhienBan).filter(SanPhamPhienBan.maphienban == id).first()
    if not obj:
        raise HTTPException(404, "Không tìm thấy phiên bản")

    for k, v in data.dict().items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj
