from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from ml.forecast_product import forecast_product

router = APIRouter(prefix="/forecast", tags=["Dự báo theo sản phẩm"])

@router.get("/sanpham/{masanpham}")
def du_bao_san_pham(
    masanpham: int,
    so_thang: int = 12,
    db: Session = Depends(get_db)
):
    result = forecast_product(db, masanpham, so_thang)

    if result is None:
        raise HTTPException(404, "Không có dữ liệu bán hàng cho sản phẩm này")

    return result.to_dict(orient="records")
