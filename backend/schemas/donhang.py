from pydantic import BaseModel
from typing import Optional
from datetime import date

class DonHangBase(BaseModel):
    makh: Optional[str] = None
    matruong: Optional[int] = None
    ngay: date
    tongtien: float
    trangthai: str

class DonHangCreate(BaseModel):
    hoten: str | None = None
    sdt: str | None = None
    diachi: str | None = None
    matruong: int | None = None
    cart: dict
    is_school: bool = False


class DonHangResponse(DonHangBase):
    madon: int

    class Config:
        from_attributes = True
