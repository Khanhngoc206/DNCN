from fastapi import APIRouter, HTTPException, Depends
import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from models.taikhoan import TaiKhoan
from models.truonghoc import TruongHoc
from schemas.taikhoan import LoginRequest, RegisterRequest, TaiKhoanResponse
from utils.jwt_token import create_access_token
from schemas.auth import LoginSchema
from schemas.taikhoan import LoginRequest, RegisterRequest, TaiKhoanResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


# ============================================
# ĐĂNG KÝ
# ============================================
@router.post("/register", response_model=TaiKhoanResponse)
def register(data: RegisterRequest, db: Session = Depends(get_db)):

    old = db.query(TaiKhoan).filter(TaiKhoan.username == data.username).first()
    if old:
        raise HTTPException(400, "Tài khoản đã tồn tại")

    hashed = pwd.hash(data.password)

    new = TaiKhoan(
        username=data.username,
        password_hash=hashed,
        role=data.role
    )

    db.add(new)
    db.commit()
    db.refresh(new)
    return new


# ============================================
# ĐĂNG NHẬP
# ============================================
@router.post("/login", response_model=dict)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(TaiKhoan).filter(TaiKhoan.username == data.username).first()

    if not user:
        raise HTTPException(400, "Sai tài khoản hoặc mật khẩu")

    if not pwd.verify(data.password, user.password_hash):
        raise HTTPException(400, "Sai tài khoản hoặc mật khẩu")

    token = jwt.encode(
        {"username": user.username, "role": user.role},
        "SECRET_KEY",
        algorithm="HS256"
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "username": user.username
    }
# ================================================
# 🎓 ĐĂNG KÝ TÀI KHOẢN TRƯỜNG HỌC
# ================================================
@router.post("/create_school_account")
def create_school_account(
    matr: int,
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    school = db.query(TruongHoc).filter(TruongHoc.matruong == matr).first()
    if not school:
        raise HTTPException(404, "Mã trường không tồn tại")

    exist = db.query(TaiKhoan).filter(TaiKhoan.username == username).first()
    if exist:
        raise HTTPException(400, "Username đã tồn tại")

    hashed = pwd.hash(password)

    new_acc = TaiKhoan(
        username=username,
        password_hash=hashed,
        role="school",
        trangthai=True,
        matruong=matr                   # ⭐ LIÊN KẾT ĐÚNG
    )

    db.add(new_acc)
    db.commit()
    db.refresh(new_acc)

    return {
        "message": "Tạo tài khoản trường thành công",
        "username": username,
        "tentruong": school.tentruong
    }


# ================================================
# 🎓 ĐĂNG NHẬP TÀI KHOẢN TRƯỜNG HỌC
# ================================================
@router.post("/login_school")
def login_school(data: LoginSchema, db: Session = Depends(get_db)):

    # tìm tài khoản trường học
    acc = db.query(TaiKhoan).filter(
        TaiKhoan.username == data.username,
        TaiKhoan.role == "school",
        TaiKhoan.trangthai == True
    ).first()

    if not acc:
        raise HTTPException(400, "Sai tài khoản hoặc mật khẩu")

    if not pwd.verify(data.password, acc.password_hash):
        raise HTTPException(400, "Sai tài khoản hoặc mật khẩu")

    # lấy trường tương ứng
    school = db.query(TruongHoc).filter(
        TruongHoc.matruong == acc.matruong
    ).first()

    if not school:
        raise HTTPException(400, "Không tìm thấy trường học")

    # tạo token
    token = create_access_token({
        "role": "school",
        "username": acc.username,
        "matruong": school.matruong
    })

    return {
        "access_token": token,
        "role": "school",
        "matruong": school.matruong,
        "tentruong": school.tentruong
    }
