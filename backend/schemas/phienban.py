from pydantic import BaseModel

class PhienBanBase(BaseModel):
    masanpham: int
    makhoi: int | None = None
    mausac: str | None = None
    ghichu: str | None = None

class PhienBanCreate(PhienBanBase):
    pass

class PhienBanResponse(PhienBanBase):
    maphienban: int

    class Config:
        from_attributes = True
