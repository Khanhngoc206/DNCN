from sqlalchemy import Column, Integer, String, Numeric
from database import Base
class SanPham(Base):
    __tablename__ = "sanpham"
    __table_args__ = {"schema": "giaodich"}

    masanpham = Column(Integer, primary_key=True, index=True)
    tensanpham = Column(String)
    danhmuc = Column(String)
    giaban = Column(Numeric)
    mota = Column(String)
    hinhanh = Column(String(255), nullable=True)  # ⭐ NEW

