from sqlalchemy import Column, Integer, ForeignKey, String
from backend.database import Base

class SizePhienBan(Base):
    __tablename__ = "size_phienban"
    __table_args__ = {"schema": "giaodich"}

    masize = Column(Integer, primary_key=True, index=True)
    maphienban = Column(Integer, ForeignKey("giaodich.sanpham_phienban.maphienban"))
    tensize = Column(String(10))
    soluongton = Column(Integer, default=0)
