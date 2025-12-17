import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

API_BASE = "http://127.0.0.1:8000"

# ============================================================
# 1. FORM LOGIN TRƯỜNG
# ============================================================
def school_login(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")

        res = requests.post(f"{API_BASE}/auth/login_school",
                            json={"username": u, "password": p})

        if res.status_code != 200:
            return render(request, "school_login.html", {"error": "Sai tài khoản hoặc mật khẩu"})

        data = res.json()

        request.session["school_logged_in"] = True
        request.session["school_token"] = data["access_token"]
        request.session["school_name"] = data["tentruong"]
        request.session["matruong"] = data["matruong"]

        return redirect("/school/home/")

    return render(request, "school_login.html")


# ============================================================
# 2. TRANG HOME TRƯỜNG
# ============================================================
def school_home(request):
    if not request.session.get("school_logged_in"):
        return redirect("/school/login/")
    return render(request, "school_home.html",
                  {"tentruong": request.session.get("school_name")})


# ============================================================
# 3. TRANG ĐẶT SỐ LƯỢNG LỚN
# ============================================================
def school_order(request):
    if not request.session.get("school_logged_in"):
        return redirect("/school/login/")

    sp = requests.get(f"{API_BASE}/sanpham/").json()

    return render(request, "school_order.html", {
        "products": sp,
        "school_name": request.session.get("school_name")
    })


# ============================================================
# 4. GỬI ĐƠN HÀNG (POST → FastAPI)
# ============================================================
def school_order_submit(request):
    if not request.session.get("school_logged_in"):
        return JsonResponse({"error": "Not logged in"}, status=403)

    data = json.loads(request.body)

    payload = {
        "matruong": request.session["matruong"],
        "is_school": True,
        "cart": data["cart"]
    }

    res = requests.post(
        f"{API_BASE}/donhang/dat_hang_truong",
        json=payload
    )

    if res.status_code == 200:
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Lỗi gửi đơn"}, status=400)


# ============================================================
# 5. LOGOUT
# ============================================================
def school_logout(request):
    request.session.flush()
    return redirect("/school/login/")
