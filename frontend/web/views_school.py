import json
import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse

API_BASE = "https://dncn-backend.onrender.com"


def school_login(request):
    if request.method == "POST":
        try:
            res = requests.post(
                f"{API_BASE}/auth/login_school",
                json={
                    "username": request.POST.get("username"),
                    "password": request.POST.get("password")
                },
                timeout=15
            )
        except:
            return render(request, "school_login.html", {"error": "Không kết nối backend"})

        if res.status_code != 200:
            return render(request, "school_login.html", {"error": "Sai tài khoản"})

        data = res.json()
        request.session["school_logged_in"] = True
        request.session["school_token"] = data["access_token"]
        request.session["school_name"] = data["tentruong"]
        request.session["matruong"] = data["matruong"]
        request.session["role"] = "school"

        return redirect("/school/home/")

    return render(request, "school_login.html")


def school_home(request):
    if not request.session.get("school_logged_in"):
        return redirect("/school/login/")
    return render(request, "school_home.html")


def school_order(request):
    if not request.session.get("school_logged_in"):
        return redirect("/school/login/")

    sp = requests.get(f"{API_BASE}/sanpham/").json()
    return render(request, "school_order.html", {"products": sp})


def school_order_submit(request):
    if not request.session.get("school_logged_in"):
        return JsonResponse({"error": "Not login"}, status=403)

    data = json.loads(request.body)
    payload = {
        "is_school": True,
        "matruong": request.session["matruong"],
        "cart": data["cart"]
    }

    res = requests.post(f"{API_BASE}/donhang/", json=payload)
    return JsonResponse({"success": res.status_code == 200})


def school_logout(request):
    request.session.flush()
    return redirect("/school/login/")
