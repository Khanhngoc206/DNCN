from pydantic import BaseModel

# Base dùng chung
class KhoiLopBase(BaseModel):
    matruong: int
    tenkhoi: str
    mausac_aotheduc: str

# Khi tạo mới
class KhoiLopCreate(KhoiLopBase):
    pass

# Khi trả về
class KhoiLopResponse(KhoiLopBase):
    makhoi: int

    class Config:
        from_attributes = True   # CHUẨN Pydantic v2
