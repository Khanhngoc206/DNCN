from sqlalchemy import Column, Integer, Numeric, String, ForeignKey
from database import Base

class ChiTietDonHang(Base):
    __tablename__ = "chitiet_donhang"
    __table_args__ = {"schema": "giaodich"}

    machitiet = Column(Integer, primary_key=True, index=True)
    madon = Column(
    Integer,
    ForeignKey("giaodich.donhang.madon"),  # ✅ ĐÚNG KHÓA CHÍNH
    nullable=False
)

    makhoi = Column(Integer)              # ✅ BẮT BUỘC
    maphienban = Column(
    Integer,
    ForeignKey("giaodich.sanpham_phienban.maphienban"),  # ✅ ĐÚNG
    nullable=False
)

    tensize = Column(String)
    soluong = Column(Integer)
    dongia = Column(Numeric)
