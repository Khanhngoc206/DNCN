from fastapi import APIRouter
from backend.ml.predictor_forecast import du_bao_nam

router = APIRouter(prefix="/forecast", tags=["Dự báo nhu cầu"])

@router.get("/nam")
def forecast_nam(so_thang: int = 12):
    result = du_bao_nam(so_thang)
    return result.to_dict(orient="records")
