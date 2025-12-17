from pydantic import BaseModel

class SizePredictRequest(BaseModel):
    chieucao: float
    cannang: float
    gioitinh: int   # 0=female, 1=male

class SizePredictResponse(BaseModel):
    size: str
