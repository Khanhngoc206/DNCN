from fastapi import APIRouter
from backend.schemas.dudoan import SizePredictRequest, SizePredictResponse
from backend.ml.predictor import predict_size

router = APIRouter(prefix="/dudoan", tags=["Dự đoán size"])

@router.post("/size", response_model=SizePredictResponse)
def du_doan_size(data: SizePredictRequest):
    size = predict_size(
        chieucao=data.chieucao,
        cannang=data.cannang,
        gioitinh=data.gioitinh
    )
    return {"size": size}
