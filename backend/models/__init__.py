from backend.database import Base

from .truonghoc import TruongHoc
from .khoilop import KhoiLop
from .sanpham import SanPham
from .donhang import DonHang
from .chitiet_donhang import ChiTietDonHang
from .phienban import SanPhamPhienBan
from .size import SizePhienBan

__all__ = [
    "Base",
    "TruongHoc",
    "KhoiLop",
    "SanPham",
    "DonHang",
    "ChiTietDonHang",
    "SanPhamPhienBan",
    "SizePhienBan",
]
