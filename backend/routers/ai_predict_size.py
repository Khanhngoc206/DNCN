from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/predict", tags=["AI Dự báo"])

@router.get("/size")
def predict_size(db: Session = Depends(get_db), matruong: int | None = None):
    """
    Dự báo số lượng size theo tháng
    Nếu matruong != None → dự báo theo từng trường học.
    """

    # Fake model (test) — sau này thay bằng model AI thật
    labels = ["2024-01", "2024-02", "2024-03", "2024-04"]

    S = [120, 130, 140, 150]
    M = [200, 220, 210, 230]
    L = [160, 150, 155, 165]
    XL = [110, 115, 120, 130]

    return {
        "labels": labels,
        "S": S,
        "M": M,
        "L": L,
        "XL": XL
    }
