from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class KhoiLop(Base):
    __tablename__ = "khoilop"
    __table_args__ = {"schema": "giaodich"}

    makhoi = Column(Integer, primary_key=True)
    matruong = Column(Integer, ForeignKey("giaodich.truonghoc.id"))
    tenkhoi = Column(String)
    mausac_aotheduc = Column(String)
