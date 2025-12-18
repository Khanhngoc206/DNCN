import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

# =========================
# ✅ API BACKEND (Render)
# =========================
API = "https://dncn-backend.onrender.com"   # <-- đổi đúng backend của bạn


# =========================================================
# ✅ SAFE REQUEST HELPERS (tránh 500 trên Render)
# =========================================================
def safe_get(url, headers=None, params=None, timeout=10):
    try:
        return requests.get(url, headers=headers, params=params, timeout=timeout)
    except Exception:
        return None


def safe_post(url, json_data=None, headers=None, timeout=10):
    try:
        return requests.post(url, json=json_data, headers=headers, timeout=timeout)
    except Exception:
        return None


def safe_put(url, json_data=None, headers=None, timeout=10):
    try:
        return requests.put(url, json=json_data, headers=headers, timeout=timeout)
    except Exception:
        return None


def safe_delete(url, headers=None, timeout=10):
    try:
        return requests.delete(url, headers=headers, timeout=timeout)
    except Exception:
        return None


def safe_json(res, default=None):
    """
    Render production rất dễ gặp response không phải JSON (HTML/empty) → .json() sẽ nổ 500.
    """
    if default is None:
        default = []
    try:
        if res and res.status_code == 200:
            return res.json()
    except Exception:
        return default
    return default


# =====================================================================
# 🚀 HOME / PRODUCT LIST
# =====================================================================
def home(request):
    res = safe_get(f"{API}/sanpham/")
    data = safe_json(res, [])
    return render(request, "home.html", {"ds_sanpham": data})


def product_list(request):
    res = safe_get(f"{API}/sanpham/")
    data = safe_json(res, [])
    return render(request, "product_list.html", {"ds_sanpham": data})


# ============================================================
# 🔍 CHI TIẾT SẢN PHẨM (an toàn key + sizes)
# ============================================================
def product_detail(request, id):
    res = safe_get(f"{API}/sanpham/{id}")
    sp = safe_json(res, None)

    if not sp:
        return render(request, "product.html", {"sp": None, "error": "Không tìm thấy sản phẩm"})

    data = {
        "masanpham": sp.get("masanpham"),
        "tensanpham": sp.get("tensanpham", ""),
        "giaban": sp.get("giaban", 0),
        "mota": sp.get("mota", ""),
        "hinhanh": sp.get("hinhanh", ""),
        "gallery": sp.get("gallery", []),
        "sizes": sp.get("sizes", ["S", "M", "L", "XL"]),
    }
    return render(request, "product.html", {"sp": data})


# ============================================================
# 🛒 CART (add theo size, key = masp_size)
# ============================================================
def add_to_cart(request, id):
    cart = request.session.get("cart", {})

    res = safe_get(f"{API}/sanpham/{id}")
    sp = safe_json(res, None)
    if not sp:
        return redirect("/")

    masp = str(sp.get("masanpham", id))
    size = request.POST.get("size", "M")  # nếu template bắt buộc chọn size thì sẽ luôn có
    key = f"{masp}_{size}"

    if key in cart:
        cart[key]["soluong"] += 1
    else:
        cart[key] = {
            "tensanpham": sp.get("tensanpham", ""),
            "hinhanh": sp.get("hinhanh", ""),
            "giaban": sp.get("giaban", 0),
            "soluong": 1,
            "size": size,
        }

    request.session["cart"] = cart
    return redirect("/cart/")


def cart(request):
    cart_data = request.session.get("cart", {})
    cart_items = []
    tong = 0

    for key, item in cart_data.items():
        gia = int(item.get("giaban", 0))
        soluong = int(item.get("soluong", 0))
        thanhtien = gia * soluong
        tong += thanhtien

        cart_items.append({
            "key": key,
            "masanpham": key.split("_")[0],
            "tensanpham": item.get("tensanpham", ""),
            "hinhanh": item.get("hinhanh", ""),
            "giaban": gia,
            "soluong": soluong,
            "size": item.get("size", "M"),
            "thanhtien": thanhtien
        })

    return render(request, "cart.html", {"cart_items": cart_items, "tongtien": tong})


def increase_qty(request, key):
    cart_data = request.session.get("cart", {})
    key = str(key)
    if key in cart_data:
        cart_data[key]["soluong"] += 1
    request.session["cart"] = cart_data
    return redirect("/cart/")


def decrease_qty(request, key):
    cart_data = request.session.get("cart", {})
    key = str(key)
    if key in cart_data:
        cart_data[key]["soluong"] -= 1
        if cart_data[key]["soluong"] <= 0:
            del cart_data[key]
    request.session["cart"] = cart_data
    return redirect("/cart/")


def remove_from_cart(request, key):
    cart_data = request.session.get("cart", {})
    key = str(key)
    if key in cart_data:
        del cart_data[key]
    request.session["cart"] = cart_data
    return redirect("/cart/")


# =====================================================================
# 💳 CHECKOUT – khách lẻ + trường
# =====================================================================
def checkout(request):
    cart_data = request.session.get("cart", {})
    if not cart_data:
        return redirect("/cart/")

    role = request.session.get("role")

    # ============================
    # 🎓 TRƯỜNG HỌC
    # ============================
    if role == "school":
        token = request.session.get("school_token")
        matruong = request.session.get("matruong")

        if request.method == "POST":
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"

            payload = {
                "is_school": True,
                "matruong": matruong,
                "cart": cart_data,
            }
            res = safe_post(f"{API}/donhang/dat_hang_truong", json_data=payload, headers=headers)
            if res and res.status_code == 200:
                request.session["cart"] = {}
                return redirect("/success/")

            messages.error(request, "Lỗi đặt hàng trường học")
        return render(request, "checkout_school.html", {"cart": cart_data})

    # ============================
    # 👤 KHÁCH LẺ
    # ============================
    return redirect("/checkout/khachle/")


def checkout_khachle(request):
    cart_data = request.session.get("cart", {})
    if not cart_data:
        messages.error(request, "Giỏ hàng đang trống!")
        return redirect("/cart/")

    cart_json = json.dumps(cart_data)

    if request.method == "POST":
        hoten = request.POST.get("hoten")
        sdt = request.POST.get("sdt")
        diachi = request.POST.get("diachi")

        try:
            cart_from_hidden = json.loads(request.POST.get("cart_json", "{}"))
        except Exception:
            cart_from_hidden = cart_data

        payload = {
            "hoten": hoten,
            "sdt": sdt,
            "diachi": diachi,
            "cart": cart_from_hidden,
        }

        # ✅ đúng endpoint khách lẻ
        res = safe_post(f"{API}/donhang/khachle", json_data=payload)

        if res and res.status_code == 200:
            request.session["cart"] = {}
            messages.success(request, "Đặt hàng thành công!")
            return redirect("/success/")

        # cố lấy message lỗi
        err_data = safe_json(res, {})
        messages.error(request, f"Lỗi đặt hàng: {err_data if err_data else 'Không rõ lỗi'}")

    return render(request, "checkout_le.html", {"cart": cart_data, "cart_json": cart_json})


def success(request):
    return render(request, "success.html")


# ==========================
# 🤖 DỰ ĐOÁN SIZE
# ==========================
def predict_size(request):
    ketqua = None
    error = None

    if request.method == "POST":
        try:
            chieucao = float(request.POST.get("chieucao"))
            cannang = float(request.POST.get("cannang"))
            gioitinh = request.POST.get("gioitinh")  # backend của bạn nhận string hay int thì tùy, bạn đang dùng string ở file cũ

            res = safe_post(f"{API}/dudoan/size", json_data={
                "chieucao": chieucao,
                "cannang": cannang,
                "gioitinh": gioitinh
            })

            if res and res.status_code == 200:
                data = safe_json(res, {})
                ketqua = data.get("size")
            else:
                error = "Không thể dự đoán size."
        except Exception as e:
            error = str(e)

    return render(request, "predict_size.html", {"ketqua": ketqua, "error": error})





# =====================================================================
# 🛠 ADMIN LOGIN + ADMIN PAGES
# =====================================================================
def admin_login(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = (request.POST.get("password") or "").strip()

        if not username or not password:
            return render(request, "admin/admin_login.html", {"error": "Vui lòng nhập đủ thông tin"})

        res = safe_post(f"{API}/auth/login", json_data={"username": username, "password": password})
        if not res or res.status_code != 200:
            return render(request, "admin/admin_login.html", {"error": "Sai tài khoản hoặc mật khẩu"})

        data = safe_json(res, {})
        if not data.get("access_token"):
            return render(request, "admin/admin_login.html", {"error": "Lỗi đăng nhập"})

        if data.get("role") != "admin":
            return render(request, "admin/admin_login.html", {"error": "Bạn không có quyền truy cập admin!"})

        request.session["token"] = data["access_token"]
        request.session["role"] = "admin"
        request.session["username"] = data.get("username", username)

        return redirect("/admin/dashboard/")

    return render(request, "admin/admin_login.html")


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.session.get("role") != "admin":
            return redirect("/admin/login/")
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    rev = safe_json(safe_get(f"{API}/thongke/revenue"), {})
    size_stat = safe_json(safe_get(f"{API}/thongke/size"), {})
    tong_doanh_thu = safe_json(safe_get(f"{API}/thongke/tong_doanh_thu"), {})
    tong_don_hang = safe_json(safe_get(f"{API}/thongke/tong_don_hang"), {})
    size_max = safe_json(safe_get(f"{API}/thongke/size_max"), {})
    best_product = safe_json(safe_get(f"{API}/thongke/best_product"), {})

    return render(request, "admin/admin_dashboard.html", {
        "labels_rev": rev.get("labels", []),
        "values_rev": rev.get("values", []),
        "labels_size": size_stat.get("labels", []),
        "values_size": size_stat.get("values", []),
        "tong_doanh_thu": tong_doanh_thu.get("total", 0),
        "tong_don_hang": tong_don_hang.get("total", 0),
        "size_max": size_max.get("size", "-"),
        "best_product": best_product.get("sanpham", "-"),
    })


@admin_required
def admin_truong(request):
    ds = safe_json(safe_get(f"{API}/truonghoc/"), [])
    return render(request, "admin/admin_truong.html", {"ds_truong": ds})


@admin_required
def admin_truong_update(request):
    if request.method == "POST":
        matr = request.POST.get("matr")
        tentruong = request.POST.get("tentruong")
        diachi = request.POST.get("diachi")
        safe_put(f"{API}/truonghoc/{matr}", json_data={"tentruong": tentruong, "diachi": diachi})
    return redirect("/admin/truong/")


@admin_required
def admin_truong_delete(request):
    if request.method == "POST":
        matr = request.POST.get("matr")
        safe_delete(f"{API}/truonghoc/{matr}")
    return redirect("/admin/truong/")


@admin_required
def admin_sanpham(request):
    ds = safe_json(safe_get(f"{API}/sanpham/"), [])
    return render(request, "admin/admin_sanpham.html", {"ds_sanpham": ds})


@admin_required
def admin_sanpham_update(request):
    if request.method == "POST":
        sid = request.POST.get("id")
        ten = request.POST.get("ten")
        gia = request.POST.get("gia")
        hinhanh = request.POST.get("hinhanh")

        # backend bạn nhận keys gì thì giữ đúng keys backend
        safe_put(f"{API}/sanpham/{sid}", json_data={
            "tensanpham": ten,
            "giaban": gia,
            "hinhanh": hinhanh
        })
    return redirect("/admin/sanpham/")


@admin_required
def admin_sanpham_delete(request):
    if request.method == "POST":
        sid = request.POST.get("id")
        safe_delete(f"{API}/sanpham/{sid}")
    return redirect("/admin/sanpham/")


@admin_required
def admin_phienban(request):
    ds = safe_json(safe_get(f"{API}/phienban/"), [])
    ds_sp = safe_json(safe_get(f"{API}/sanpham/"), [])
    return render(request, "admin/admin_phienban.html", {"ds_phienban": ds, "ds_sanpham": ds_sp})


@admin_required
def admin_size(request):
    ds = safe_json(safe_get(f"{API}/size/"), [])
    ds_pb = safe_json(safe_get(f"{API}/phienban/"), [])
    return render(request, "admin/admin_size.html", {"ds_size": ds, "ds_phienban": ds_pb})


@admin_required
def admin_donhang(request):
    ds = safe_json(safe_get(f"{API}/donhang/"), [])
    return render(request, "admin/admin_donhang.html", {"ds_donhang": ds})


@admin_required
def admin_donhang_chitiet(request, id):
    res = safe_get(f"{API}/donhang/{id}")
    if not res or res.status_code != 200:
        return JsonResponse({"error": "Không tìm thấy đơn hàng"}, status=404)
    return JsonResponse(safe_json(res, {}), safe=False)


@admin_required
def admin_logout(request):
    request.session.flush()
    return redirect("/admin/login/")
@admin_required
def admin_ai_model(request):
    token = request.session.get("token")

    # 🔹 Danh sách sản phẩm
    sp_res = safe_get("/sanpham/")
    ds_sanpham = sp_res.json() if sp_res.status_code == 200 else []

    masanpham = request.GET.get("masanpham")

    labels, S, M, L, XL = [], [], [], [], []

    if masanpham:
        forecast_res = safe_get(
            f"/forecast/sanpham/{masanpham}",
            params={"so_thang": 12}
        )

        if forecast_res.status_code == 200:
            for row in forecast_res.json():
                labels.append(row.get("thang"))
                S.append(row.get("S", 0))
                M.append(row.get("M", 0))
                L.append(row.get("L", 0))
                XL.append(row.get("XL", 0))

    return render(request, "admin/admin_ai_model.html", {
        "ds_sanpham": ds_sanpham,
        "masanpham": masanpham,
        "labels": labels,
        "S": S,
        "M": M,
        "L": L,
        "XL": XL,
    })
