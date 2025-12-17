from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from database import Base

class TaiKhoan(Base):
    __tablename__ = "taikhoan"

    mataikhoan = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="admin")
    trangthai = Column(Boolean, default=True)
    matruong = Column(Integer, nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)
