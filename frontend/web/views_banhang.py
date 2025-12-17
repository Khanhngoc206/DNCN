import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

API = "https://uniform-api.onrender.com"

# =====================================================================
# 🚀 TRANG CHÍNH – HOME
# =====================================================================
def home(request):
    res = requests.get(f"{API}/sanpham/")
    data = res.json() if res.status_code == 200 else []

    return render(request, "home.html", {"ds_sanpham": data})

def product_list(request):
    res = requests.get(f"{API}/sanpham/")
    data = res.json() if res.status_code == 200 else []
    return render(request, "product_list.html", {"ds_sanpham": data})

# ============================================================
# 🔍 CHI TIẾT SẢN PHẨM
# ============================================================
def product_detail(request, id):
    res = requests.get(f"{API}/sanpham/{id}")

    if res.status_code != 200:
        return render(request, "product.html", {"sp": None})

    sp = res.json()

    data = {
        "masanpham": sp["masanpham"],
        "tensanpham": sp["tensanpham"],
        "giaban": sp["giaban"],
        "mota": sp["mota"],
        "hinhanh": sp["hinhanh"],
        "gallery": sp.get("gallery", []),
        "sizes": sp.get("sizes", ["S", "M", "L", "XL"])
    }

    return render(request, "product.html", {"sp": data})




# ============================================================
# 🛒 THÊM VÀO GIỎ HÀNG
# ============================================================
def add_to_cart(request, id):
    cart = request.session.get("cart", {})

    res = requests.get(f"{API}/sanpham/{id}")
    if res.status_code != 200:
        return redirect("/")

    sp = res.json()
    masp = str(sp["masanpham"])

    # Lấy size từ POST (mặc định M nếu không chọn)
    size = request.POST.get("size", "M")

    key = f"{masp}_{size}"  # phân biệt sản phẩm theo size

    if key in cart:
        cart[key]["soluong"] += 1
    else:
        cart[key] = {
            "tensanpham": sp["tensanpham"],
            "hinhanh": sp["hinhanh"],
            "giaban": sp["giaban"],
            "soluong": 1,
            "size": size,
        }

    request.session["cart"] = cart
    return redirect("/cart/")

# =====================================================================
# 🛒 TRANG GIỎ HÀNG
# =====================================================================
def cart(request):
    cart = request.session.get("cart", {})

    cart_items = []
    tong = 0

    for key, item in cart.items():
        gia = item["giaban"]
        soluong = item["soluong"]
        thanhtien = gia * soluong
        tong += thanhtien

        cart_items.append({
            "key": key,  # ✔ dùng key để tăng/giảm đúng size
            "masanpham": key.split("_")[0],
            "tensanpham": item["tensanpham"],
            "hinhanh": item["hinhanh"],
            "giaban": gia,
            "soluong": soluong,
            "size": item["size"],  # ✔ thêm size
            "thanhtien": thanhtien
        })

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "tongtien": tong
    })

# =====================================================================
# 🛒 XÓA SẢN PHẨM KHỎI GIỎ
# =====================================================================
def increase_qty(request, key):
    cart = request.session.get("cart", {})
    key = str(key)
    if key in cart:
        cart[key]["soluong"] += 1
    request.session["cart"] = cart
    return redirect("/cart/")


def decrease_qty(request, key):
    cart = request.session.get("cart", {})
    key = str(key)
    if key in cart:
        cart[key]["soluong"] -= 1
        if cart[key]["soluong"] <= 0:
            del cart[key]
    request.session["cart"] = cart
    return redirect("/cart/")


def remove_from_cart(request, key):
    cart = request.session.get("cart", {})
    key = str(key)
    if key in cart:
        del cart[key]
    request.session["cart"] = cart
    return redirect("/cart/")



# =====================================================================
# 💳 CHECKOUT – KHÁCH LẺ + TRƯỜNG HỌC
# =====================================================================
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("/cart/")

    role = request.session.get("role")

    # ============================
    # 🎓 TRƯỜNG HỌC
    # ============================
    if role == "school":
        token = request.session.get("school_token")
        matruong = request.session.get("matruong")

        if request.method == "POST":
            res = requests.post(
                f"{API}/donhang/",
                json={
                    "is_school": True,
                    "matruong": matruong,
                    "cart": cart
                },
                headers={"Authorization": f"Bearer {token}"}
            )

            if res.status_code == 200:
                request.session["cart"] = {}
                return redirect("/success/")

        return render(request, "checkout_school.html", {"cart": cart})

    # ============================
    # 👤 KHÁCH LẺ → CHUYỂN SANG checkout_khachle
    # ============================
    
    return redirect("/checkout/khachle/")


def checkout_khachle(request):
    cart = request.session.get("cart", {})

    if not cart:
        messages.error(request, "Giỏ hàng đang trống!")
        return redirect("/cart/")

    cart_json = json.dumps(cart)

    if request.method == "POST":
        hoten = request.POST.get("hoten")
        sdt = request.POST.get("sdt")
        diachi = request.POST.get("diachi")
        cart_data = json.loads(request.POST.get("cart_json"))

        payload = {
            "hoten": hoten,
            "sdt": sdt,
            "diachi": diachi,
            "cart": cart_data,
        }

        try:
            res = requests.post(API, json=payload)
            data = res.json()

            if res.status_code == 200:
                request.session["cart"] = {}
                messages.success(request, "Đặt hàng thành công!")
                return redirect("/thankyou/")

            else:
                messages.error(request, f"Lỗi đặt hàng: {data}")
        except Exception as e:
            messages.error(request, f"Lỗi kết nối API: {e}")

    return render(request, "checkout_le.html", {
        "cart": cart,
        "cart_json": cart_json
    })



# ==========================
# DỰ ĐOÁN SIZE
# ==========================
def predict_size(request):
    ketqua = None
    error = None

    if request.method == "POST":
        chieucao = float(request.POST.get("chieucao"))
        cannang = float(request.POST.get("cannang"))
        gioitinh = 1 if request.POST.get("gioitinh") == "Nam" else 0

        res = requests.post(f"{API}/dudoan/size", json={
            "chieucao": chieucao,
            "cannang": cannang,
            "gioitinh": gioitinh
        })

        if res.status_code == 200:
            ketqua = res.json().get("size")
        else:
            error = "Không thể dự đoán size."

    return render(request, "predict_size.html", {
        "ketqua": ketqua,
        "error": error
    })



def success(request):
    return render(request, "banhang/success.html")


# =====================================================================
# 🛠 ADMIN LOGIN
# =====================================================================
def admin_login(request):
    error = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        res = requests.post(f"{API}/auth/login", json={
            "username": username,
            "password": password,
        })

        if res.status_code != 200:
            error = "Sai tài khoản hoặc mật khẩu"
            return render(request, "admin/admin_login.html", {"error": error})

        data = res.json()

        if "access_token" not in data:
            error = "Lỗi đăng nhập"
            return render(request, "admin/admin_login.html", {"error": error})

        request.session["token"] = data["access_token"]
        request.session["role"] = data["role"]
        request.session["username"] = data["username"]

        if data["role"] != "admin":
            error = "Bạn không có quyền truy cập admin!"
            return render(request, "admin/admin_login.html", {"error": error})

        return redirect("/admin/dashboard/")

    return render(request, "admin/admin_login.html", {"error": error})


# =====================================================================
# 📊 ADMIN DASHBOARD
# =====================================================================
def admin_dashboard(request):
    if request.session.get("role") != "admin":
        return redirect("/admin/login/")

    rev = requests.get(f"{API}/thongke/revenue").json()
    size_stat = requests.get(f"{API}/thongke/size").json()
    tong_doanh_thu = requests.get(f"{API}/thongke/tong_doanh_thu").json()
    tong_don_hang = requests.get(f"{API}/thongke/tong_don_hang").json()
    size_max = requests.get(f"{API}/thongke/size_max").json()
    best_product = requests.get(f"{API}/thongke/best_product").json()

    return render(request, "admin/admin_dashboard.html", {
        "labels_rev": rev.get("labels", []),
        "values_rev": rev.get("values", []),

        "labels_size": size_stat.get("labels", []),
        "values_size": size_stat.get("values", []),

        "tong_doanh_thu": tong_doanh_thu.get("total", 0),
        "tong_don_hang": tong_don_hang.get("total", 0),
        "size_max": size_max.get("size", "-"),
        "best_product": best_product.get("sanpham", "-")
    })




# =====================================================================
# 🏫 ADMIN TRƯỜNG HỌC
# =====================================================================
def admin_truong(request):
    if request.session.get("role") != "admin":
        return redirect("/admin/login/")

    ds = requests.get(f"{API}/truonghoc/").json()
    return render(request, "admin/admin_truong.html", {"ds_truong": ds})


def admin_truong_update(request):
    if request.method == "POST":
        matr = request.POST.get("matr")
        tentruong = request.POST.get("tentruong")
        diachi = request.POST.get("diachi")

        requests.put(f"{API}/truonghoc/{matr}", json={
            "tentruong": tentruong,
            "diachi": diachi
        })

    return redirect("/admin/truong/")


def admin_truong_delete(request):
    if request.method == "POST":
        matr = request.POST.get("matr")
        requests.delete(f"{API}/truonghoc/{matr}")

    return redirect("/admin/truong/")


# =====================================================================
# 🛍 ADMIN SẢN PHẨM
# =====================================================================
def admin_sanpham(request):
    if request.session.get("role") != "admin":
        return redirect("/admin/login/")

    ds = requests.get(f"{API}/sanpham/").json()
    return render(request, "admin/admin_sanpham.html", {"ds_sanpham": ds})


def admin_sanpham_update(request):
    if request.method == "POST":
        id = request.POST.get("id")
        ten = request.POST.get("ten")
        gia = request.POST.get("gia")
        anh = request.POST.get("anh")

        requests.put(f"{API}/sanpham/{id}", json={
            "ten": ten,
            "gia": gia,
            "anh": anh
        })

    return redirect("/admin/sanpham/")


def admin_sanpham_delete(request):
    if request.method == "POST":
        id = request.POST.get("id")
        requests.delete(f"{API}/sanpham/{id}")

    return redirect("/admin/sanpham/")


# =====================================================================
# 🎨 ADMIN PHIÊN BẢN
# =====================================================================
def admin_phienban(request):
    if request.session.get("role") != "admin":
        return redirect("/admin/login/")

    ds = requests.get(f"{API}/phienban/").json()
    ds_sp = requests.get(f"{API}/sanpham/").json()

    return render(request, "admin/admin_phienban.html", {
        "ds_phienban": ds,
        "ds_sanpham": ds_sp
    })


def admin_phienban_update(request):
    if request.method == "POST":
        id = request.POST.get("id")
        sanpham_id = request.POST.get("sanpham_id")
        mau = request.POST.get("mau")
        gia = request.POST.get("gia")
        anh = request.POST.get("anh")

        requests.put(f"{API}/phienban/{id}", json={
            "sanpham_id": int(sanpham_id),
            "mau": mau,
            "gia": float(gia),
            "anh": anh
        })

    return redirect("/admin/phienban/")


def admin_phienban_delete(request):
    if request.method == "POST":
        id = request.POST.get("id")
        requests.delete(f"{API}/phienban/{id}")

    return redirect("/admin/phienban/")


# =====================================================================
# 📏 ADMIN SIZE
# =====================================================================
def admin_size(request):
    if request.session.get("role") != "admin":
        return redirect("/admin/login/")

    ds = requests.get(f"{API}/size/").json()
    ds_pb = requests.get(f"{API}/phienban/").json()

    return render(request, "admin/admin_size.html", {
        "ds_size": ds,
        "ds_phienban": ds_pb
    })


def admin_size_update(request):
    if request.method == "POST":
        id = request.POST.get("id")
        phienban_id = request.POST.get("phienban_id")
        size = request.POST.get("size")
        tonkho = request.POST.get("tonkho")

        requests.put(f"{API}/size/{id}", json={
            "phienban_id": int(phienban_id),
            "size": size,
            "tonkho": int(tonkho)
        })

    return redirect("/admin/size/")


def admin_size_delete(request):
    if request.method == "POST":
        id = request.POST.get("id")
        requests.delete(f"{API}/size/{id}")

    return redirect("/admin/size/")


# =====================================================================
# 📦 ADMIN ĐƠN HÀNG
# =====================================================================
def admin_donhang(request):
    if request.session.get("role") != "admin":
        return redirect("/admin/login/")

    ds = requests.get(f"{API}/donhang/").json()
    return render(request, "admin/admin_donhang.html", {"ds_donhang": ds})


def admin_donhang_chitiet(request, id):
    res = requests.get(f"{API}/donhang/{id}")
    if res.status_code != 200:
        return JsonResponse({"error": "Không tìm thấy đơn hàng"}, status=404)

    return JsonResponse(res.json(), safe=False)


def admin_donhang_update_status(request):
    if request.method == "POST":
        id = request.POST.get("id")
        status = request.POST.get("trangthai", "Đang xử lý")

        requests.put(f"{API}/donhang/{id}/status", json={"trangthai": status})

    return redirect("/admin/donhang/")


def admin_donhang_delete(request):
    if request.method == "POST":
        id = request.POST.get("id")
        requests.delete(f"{API}/donhang/{id}")

    return redirect("/admin/donhang/")

# =====================================================================
# 🚪 ADMIN AI
# =====================================================================
def admin_ai_model(request):
    if request.session.get("role") != "admin":
        return redirect("/admin/login/")

    data = requests.get(f"{API}/predict/size").json()

    return render(request, "admin/admin_ai_model.html", {
        "labels": data.get("labels", []),
        "S": data.get("S", []),
        "M": data.get("M", []),
        "L": data.get("L", []),
        "XL": data.get("XL", []),
    })

# =====================================================================
# 🚪 ADMIN LOGOUT
# =====================================================================
def admin_logout(request):
    request.session.flush()
    return redirect("/admin/login/")


