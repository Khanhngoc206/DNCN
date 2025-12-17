from pydantic import BaseModel
from decimal import Decimal

class CTDonHangBase(BaseModel):
    madon: int
    maphienban: int
    tensize: str
    soluong: int
    dongia: Decimal

class CTDonHangCreate(CTDonHangBase):
    pass

class CTDonHangResponse(CTDonHangBase):
    machitiet: int
    madon: int

    class Config:
        from_attributes = True
