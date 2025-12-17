from sqlalchemy import Column, Integer, String
from database import Base

class KhachHang(Base):
    __tablename__ = "khachhang"
    __table_args__ = {"schema": "giaodich"}

    makhachhang = Column(Integer, primary_key=True, index=True)
    tenkh = Column(String(255), nullable=False)
    diachi = Column(String)
    sodienthoai = Column(String(20))
