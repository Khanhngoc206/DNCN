from pydantic import BaseModel

class KhachHangCreate(BaseModel):
    tenkh: str
    diachi: str | None = None
    sodienthoai: str | None = None

class KhachHangResponse(KhachHangCreate):
    makh: int

    class Config:
        from_attributes = True
