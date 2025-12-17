from pydantic import BaseModel

class TruongBase(BaseModel):
    tentruong: str
    diachi: str | None = None
    sodienthoai: str | None = None

class TruongCreate(TruongBase):
    username: str
    password: str

class TruongResponse(BaseModel):
    matruong: int
    tentruong: str
    diachi: str
    sodienthoai: str | None = None
    username: str | None = None   # nếu có dùng
    
    class Config:
        from_attributes = True      # cần cho Pydantic v2
