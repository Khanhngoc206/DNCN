from sqlalchemy import Column, Integer, String
from database import Base

class TruongHoc(Base):
    __tablename__ = "truonghoc"
    __table_args__ = {"schema": "giaodich"}   # ⭐️ BẮT BUỘC

    matruong = Column(Integer, primary_key=True, index=True)
    tentruong = Column(String(255), nullable=False)
    diachi = Column(String, nullable=True)
    sodienthoai = Column(String(20), nullable=True)
   