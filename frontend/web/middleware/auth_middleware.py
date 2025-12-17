from django.shortcuts import redirect

class AdminRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_paths = [
            "/admin/dashboard/",
            "/admin/truong/",
            "/admin/sanpham/",
            "/admin/phienban/",
            "/admin/size/",
            "/admin/donhang/"
        ]

        if request.path in admin_paths:
            if request.session.get("role") != "admin":
                return redirect("/admin/login/")

        return self.get_response(request)
