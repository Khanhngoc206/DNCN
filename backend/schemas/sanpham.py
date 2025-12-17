from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class SanPhamBase(BaseModel):
    tensanpham: str
    danhmuc: Optional[str] = None
    giaban: float
    mota: Optional[str] = None
    hinhanh: Optional[str] = None  # ⭐ NEW


class SanPhamCreate(SanPhamBase):
    pass


class SanPhamUpdate(BaseModel):
    tensanpham: Optional[str] = None
    danhmuc: Optional[str] = None
    giaban: Optional[float] = None
    mota: Optional[str] = None
    hinhanh: Optional[str] = None  # ⭐ NEW


class SanPhamResponse(SanPhamBase):
    masanpham: int

    class Config:
        orm_mode = True