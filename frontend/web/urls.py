from django.urls import path
from . import views_banhang
from . import views_school 

urlpatterns = [
    path("", views_banhang.home, name="home"),

    # Bán hàng
    path("product/", views_banhang.product_list, name="product_list"),
    path("sanpham/<int:id>/", views_banhang.product_detail, name="product_detail"),
    path("giohang/add/<int:id>/", views_banhang.add_to_cart),
    path("cart/", views_banhang.cart, name="cart"),
    path("cart/remove/<str:key>/", views_banhang.remove_from_cart),
    path("cart/increase/<str:key>/", views_banhang.increase_qty),
    path("cart/decrease/<str:key>/", views_banhang.decrease_qty),
    path("checkout/", views_banhang.checkout, name="checkout"),
    path("checkout/khachle/", views_banhang.checkout_khachle),
    path("success/", views_banhang.success, name="success"),
    path("predict-size/", views_banhang.predict_size, name="predict_size"),

    # School
    path("school/login/", views_school.school_login),
    path("school/logout/", views_school.school_logout),
    path("school/home/", views_school.school_home),
    path("school/order/", views_school.school_order),
    path("school/order/submit/", views_school.school_order_submit),

    # Admin
    path("admin/login/", views_banhang.admin_login),
    path("admin/dashboard/", views_banhang.admin_dashboard, name="admin_dashboard"),
    path("admin/truong/", views_banhang.admin_truong),
    path("admin/sanpham/", views_banhang.admin_sanpham),
    path("admin/phienban/", views_banhang.admin_phienban),
    path("admin/donhang/", views_banhang.admin_donhang),
    path("admin/donhang/<int:id>/", views_banhang.admin_donhang_chitiet),
    path("admin/size/", views_banhang.admin_size),
    path("admin/ai-model/", views_banhang.admin_ai_model),
    path("admin/logout/", views_banhang.admin_logout),
    path(
    "forecast/sanpham/<int:masanpham>/",
    views_banhang.forecast_product_view,
    name="forecast_product"
),

]
