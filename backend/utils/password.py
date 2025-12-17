from passlib.context import CryptContext

# Thuật toán mã hóa chuẩn dùng cho hệ thống
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Mã hóa mật khẩu
    """
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """
    Kiểm tra mật khẩu nhập vào có đúng hay không
    """
    return pwd_context.verify(password, hashed)
