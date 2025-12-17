from pydantic import BaseModel

class SizeBase(BaseModel):
    maphienban: int
    tensize: str
    soluongton: int

class SizeCreate(SizeBase):
    pass

class SizeResponse(SizeBase):
    masize: int

    class Config:
        from_attributes = True
