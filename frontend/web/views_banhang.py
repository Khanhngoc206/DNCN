import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages

API_BASE = "https://dncn-backend.onrender.com"


# ===============================
# HELPER CALL API (CHỐNG 500)
# ===============================
def api_get(path, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        return requests.get(f"{API_BASE}{path}", headers=headers, timeout=15)
    except:
        return None


def api_post(path, payload=None, token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        return requests.post(f"{API_BASE}{path}", json=payload or {}, headers=headers, timeout=15)
    except:
        return None


# ===============================
# HOME + PRODUCT
# ===============================
def home(request):
    res = api_get("/sanpham/")
    data = res.json() if res and res.status_code == 200 else []
    return render(request, "home.html", {"ds_sanpham": data})


def product_list(request):
    res = api_get("/sanpham/")
    data = res.json() if res and res.status_code == 200 else []
    return render(request, "product_list.html", {"ds_sanpham": data})


def product_detail(request, id):
    res = api_get(f"/sanpham/{id}")
    if not res or res.status_code != 200:
        return redirect("/")
    return render(request, "product.html", {"sp": res.json()})


# ===============================
# CART
# ===============================
def add_to_cart(request, id):
    cart = request.session.get("cart", {})
    res = api_get(f"/sanpham/{id}")
    if not res or res.status_code != 200:
        return redirect("/")

    sp = res.json()
    size = request.POST.get("size", "M")
    key = f"{sp['masanpham']}_{size}"

    cart[key] = {
        "tensanpham": sp["tensanpham"],
        "hinhanh": sp["hinhanh"],
        "giaban": sp["giaban"],
        "soluong": cart.get(key, {}).get("soluong", 0) + 1,
        "size": size
    }

    request.session["cart"] = cart
    return redirect("/cart/")


def cart(request):
    cart = request.session.get("cart", {})
    tong = sum(i["giaban"] * i["soluong"] for i in cart.values())
    return render(request, "cart.html", {"cart_items": cart, "tongtien": tong})


def remove_from_cart(request, key):
    cart = request.session.get("cart", {})
    cart.pop(key, None)
    request.session["cart"] = cart
    return redirect("/cart/")


# ===============================
# CHECKOUT
# ===============================
def checkout(request):
    if not request.session.get("cart"):
        return redirect("/cart/")

    if request.session.get("role") == "school":
        return render(request, "checkout_school.html")

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
            "cart": cart
        }

        res = api_post("/donhang/khachle", payload)
        if res and res.status_code == 200:
            request.session["cart"] = {}
            return redirect("/success/")

        messages.error(request, "Lỗi đặt hàng")

    return render(request, "checkout_le.html", {"cart": cart})


def success(request):
    return render(request, "success.html")


# ===============================
# ADMIN
# ===============================
def admin_login(request):
    if request.method == "POST":
        res = api_post("/auth/login", {
            "username": request.POST.get("username"),
            "password": request.POST.get("password")
        })

        if not res or res.status_code != 200:
            return render(request, "admin/admin_login.html", {"error": "Sai tài khoản"})

        data = res.json()
        if data.get("role") != "admin":
            return render(request, "admin/admin_login.html", {"error": "Không có quyền admin"})

        request.session["token"] = data["access_token"]
        request.session["role"] = "admin"
        return redirect("/admin/dashboard/")

    return render(request, "admin/admin_login.html")


def admin_dashboard(request):
    if request.session.get("role") != "admin":
        return redirect("/admin/login/")
    return render(request, "admin/admin_dashboard.html")


def admin_logout(request):
    request.session.flush()
    return redirect("/admin/login/")
