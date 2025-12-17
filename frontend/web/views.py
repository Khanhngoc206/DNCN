import requests
from django.shortcuts import render

API = API_BASE = "https://dncn-backend.onrender.com"

# ==================================
# 1. TRƯỜNG HỌC
# ==================================
def truonghoc(request):
    res = requests.get(f"{API}/truonghoc/")
    data = res.json()
    return render(request, "truonghoc.html", {"ds_truong": data})


# ==================================
# 2. KHỐI LỚP
# ==================================
def khoilop(request):
    res = requests.get(f"{API}/khoilop/")
    data = res.json()
    return render(request, "khoilop.html", {"ds_khoi": data})


# ==================================
# 3. SẢN PHẨM
# ==================================
def sanpham(request):
    res = requests.get(f"{API}/sanpham/")
    data = res.json()
    return render(request, "sanpham.html", {"ds_sanpham": data})


# ==================================
# 4. PHIÊN BẢN SẢN PHẨM
# ==================================
def phienban(request):
    res = requests.get(f"{API}/phienban/")
    data = res.json()
    return render(request, "phienban.html", {"ds_phienban": data})


# ==================================
# 5. SIZE - tồn kho
# ==================================
def size(request):
    res = requests.get(f"{API}/size/")
    data = res.json()
    return render(request, "size.html", {"ds_size": data})


# ==================================
# 6. DỰ ĐOÁN SIZE TỪ AI
# ==================================
def predict_size(request):
    ketqua = None

    if request.method == "POST":
        cc = request.POST.get("chieucao")
        cn = request.POST.get("cannang")
        gt = request.POST.get("gioitinh")

        res = requests.post(f"{API}/dudoan/", json={
            "chieucao": int(cc),
            "cannang": int(cn),
            "gioitinh": int(gt),
        })

        ketqua = res.json().get("size")

    return render(request, "predict_size.html", {"ketqua": ketqua})

