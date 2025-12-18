import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse

API = "https://dncn.onrender.com"
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

# ============================================================
# 🏫 SCHOOL (login / order)
# ============================================================
def school_login(request):
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")

        res = safe_post(f"{API}/auth/login_school", json_data={"username": u, "password": p})
        if not res or res.status_code != 200:
            return render(request, "school_login.html", {"error": "Sai tài khoản hoặc mật khẩu"})

        data = safe_json(res, {})
        request.session["school_logged_in"] = True
        request.session["role"] = "school"
        request.session["school_token"] = data.get("access_token")
        request.session["school_name"] = data.get("tentruong")
        request.session["matruong"] = data.get("matruong")
        return redirect("/school/home/")

    return render(request, "school_login.html")


def school_home(request):
    if not request.session.get("school_logged_in"):
        return redirect("/school/login/")
    return render(request, "school_home.html", {"tentruong": request.session.get("school_name")})


def school_order(request):
    if not request.session.get("school_logged_in"):
        return redirect("/school/login/")

    res = safe_get(f"{API}/sanpham/")
    sp = safe_json(res, [])

    return render(request, "school_order.html", {
        "products": sp,
        "school_name": request.session.get("school_name")
    })


def school_order_submit(request):
    if not request.session.get("school_logged_in"):
        return JsonResponse({"error": "Not logged in"}, status=403)

    try:
        data = json.loads(request.body or "{}")
    except Exception:
        data = {}

    payload = {
        "matruong": request.session.get("matruong"),
        "is_school": True,
        "cart": data.get("cart", {}),
    }

    res = safe_post(f"{API}/donhang/dat_hang_truong", json_data=payload)
    if res and res.status_code == 200:
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Lỗi gửi đơn"}, status=400)


def school_logout(request):
    request.session.flush()
    return redirect("/school/login/")