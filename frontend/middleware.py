# frontend/web/middleware.py
from django.shortcuts import redirect

class SchoolAuthMiddleware:
    """
    Nếu vào /school/* mà chưa có session school_token => đá về /school/login
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith("/school/") and not path.startswith("/school/login"):
            if not request.session.get("school_token"):
                return redirect("/school/login/")

        return self.get_response(request)
