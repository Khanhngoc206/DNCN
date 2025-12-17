from sqlalchemy import Column, Integer, ForeignKey, String, Text
from database import Base

class SanPhamPhienBan(Base):
    __tablename__ = "sanpham_phienban"
    __table_args__ = {"schema": "giaodich"}

    maphienban = Column(Integer, primary_key=True, index=True)
    masanpham = Column(Integer, ForeignKey("giaodich.sanpham.masanpham"))
    makhoi = Column(Integer, ForeignKey("giaodich.khoilop.makhoi"))
    mausac = Column(String(100))
    ghichu = Column(Text)
