import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

API_BASE = "https://dncn.onrender.com"

# ============================================================
# HOME
# ============================================================
def home(request):
    res = requests.get(f"{API_BASE}/sanpham/")
    data = res.json() if res.status_code == 200 else []
    return render(request, "home.html", {"ds_sanpham": data})


def product_list(request):
    res = requests.get(f"{API_BASE}/sanpham/")
    data = res.json() if res.status_code == 200 else []
    return render(request, "product_list.html", {"ds_sanpham": data})


def product_detail(request, id):
    res = requests.get(f"{API_BASE}/sanpham/{id}")
    if res.status_code != 200:
        return redirect("/")
    return render(request, "product.html", {"sp": res.json()})


# ============================================================
# CART
# ============================================================
def add_to_cart(request, id):
    cart = request.session.get("cart", {})
    res = requests.get(f"{API_BASE}/sanpham/{id}")
    if res.status_code != 200:
        return redirect("/")

    sp = res.json()
    size = request.POST.get("size", "M")
    key = f"{sp['masanpham']}_{size}"

    cart[key] = {
        "tensanpham": sp["tensanpham"],
        "hinhanh": sp["hinhanh"],
        "giaban": sp["giaban"],
        "soluong": cart.get(key, {}).get("soluong", 0) + 1,
        "size": size,
    }

    request.session["cart"] = cart
    return redirect("/cart/")


def cart(request):
    cart = request.session.get("cart", {})
    tong = sum(i["giaban"] * i["soluong"] for i in cart.values())
    return render(request, "cart.html", {"cart_items": cart, "tongtien": tong})


def increase_qty(request, key):
    cart = request.session.get("cart", {})
    if key in cart:
        cart[key]["soluong"] += 1
    request.session["cart"] = cart
    return redirect("/cart/")


def decrease_qty(request, key):
    cart = request.session.get("cart", {})
    if key in cart:
        cart[key]["soluong"] -= 1
        if cart[key]["soluong"] <= 0:
            del cart[key]
    request.session["cart"] = cart
    return redirect("/cart/")


def remove_from_cart(request, key):
    cart = request.session.get("cart", {})
    cart.pop(key, None)
    request.session["cart"] = cart
    return redirect("/cart/")


# ============================================================
# CHECKOUT
# ============================================================
def checkout(request):
    if not request.session.get("cart"):
        return redirect("/cart/")
    return redirect("/checkout/khachle/")


def checkout_khachle(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("/cart/")

    if request.method == "POST":
        payload = {
            "hoten": request.POST.get("hoten"),
            "sdt": request.POST.get("sdt"),
            "diachi": request.POST.get("diachi"),
            "cart": cart,
        }
        res = requests.post(f"{API_BASE}/donhang/khachle", json=payload)
        if res.status_code == 200:
            request.session["cart"] = {}
            return redirect("/success/")

        messages.error(request, "Lỗi đặt hàng")

    return render(request, "checkout_le.html", {"cart": cart})


def success(request):
    return render(request, "success.html")


# ============================================================
# AI SIZE
# ============================================================
def predict_size(request):
    ketqua = None
    error = None

    if request.method == "POST":
        try:
            res = requests.post(
                f"{API_BASE}/dudoan/size",
                json={
                    "chieucao": float(request.POST.get("chieucao")),
                    "cannang": float(request.POST.get("cannang")),
                    "gioitinh": request.POST.get("gioitinh"),
                },
                timeout=10,
            )
            if res.status_code == 200:
                ketqua = res.json().get("size")
            else:
                error = "Không dự đoán được size"
        except Exception as e:
            error = str(e)

    return render(request, "predict_size.html", {"ketqua": ketqua, "error": error})
def forecast_product_view(request, masanpham):
    try:
        res = requests.get(
            f"{API_BASE}/forecast/sanpham/{masanpham}",
            params={"so_thang": 12},
            timeout=10
        )

        if res.status_code != 200:
            return render(request, "forecast_product.html", {
                "error": "Không có dữ liệu dự báo"
            })

        data = res.json()

        return render(request, "forecast_product.html", {
            "data": data,
            "masanpham": masanpham
        })

    except Exception as e:
        return render(request, "forecast_product.html", {
            "error": str(e)
        })


# ============================================================
# ADMIN (STUB – KHÔNG 500)
# ============================================================
def admin_login(request): return render(request, "admin/admin_login.html")
def admin_dashboard(request): return render(request, "admin/admin_dashboard.html")
def admin_logout(request): request.session.flush(); return redirect("/admin/login/")

def admin_truong(request): return render(request, "admin/admin_truong.html")
def admin_sanpham(request): return render(request, "admin/admin_sanpham.html")
def admin_phienban(request): return render(request, "admin/admin_phienban.html")
def admin_donhang(request): return render(request, "admin/admin_donhang.html")
def admin_donhang_chitiet(request, id): return JsonResponse({"id": id})
def admin_size(request): return render(request, "admin/admin_size.html")
def admin_ai_model(request):
    if request.session.get("role") != "admin":
        return redirect("/admin/login/")

    # 🔹 Lấy danh sách sản phẩm cho dropdown
    sp_res = requests.get(f"{API_BASE}/sanpham/")
    ds_sanpham = sp_res.json() if sp_res.status_code == 200 else []

    masanpham = request.GET.get("masanpham")

    labels, S, M, L, XL = [], [], [], [], []

    if masanpham:
        forecast_res = requests.get(
            f"{API_BASE}/forecast/sanpham/{masanpham}",
            params={"so_thang": 12}
        )

        if forecast_res.status_code == 200:
            data = forecast_res.json()

            for row in data:
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

def admin_truong_update(request): return JsonResponse({"ok": True})
def admin_truong_delete(request): return JsonResponse({"ok": True})
def admin_sanpham_update(request): return JsonResponse({"ok": True})
def admin_sanpham_delete(request): return JsonResponse({"ok": True})
def admin_phienban_update(request): return JsonResponse({"ok": True})
def admin_phienban_delete(request): return JsonResponse({"ok": True})
def admin_size_update(request): return JsonResponse({"ok": True})
def admin_size_delete(request): return JsonResponse({"ok": True})
def admin_donhang_update_status(request): return JsonResponse({"ok": True})
def admin_donhang_delete(request): return JsonResponse({"ok": True})
