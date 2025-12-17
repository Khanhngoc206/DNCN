from sqlalchemy import Column, Integer, Date, DECIMAL, String, ForeignKey
from database import Base

class DonHang(Base):
    __tablename__ = "donhang"
    __table_args__ = {"schema": "giaodich"}

    madon = Column(Integer, primary_key=True, index=True)

    # Khách lẻ
    makh = Column(String(20), nullable=True)

    # Trường học
    matruong = Column(Integer, ForeignKey("giaodich.truonghoc.matruong"), nullable=True)

    ngaydat = Column(Date)   # 🔥 tên đúng trong PostgreSQL
    tongtien = Column(DECIMAL)
    trangthai = Column(String(20))
