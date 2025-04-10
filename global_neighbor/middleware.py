from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse


class BlockPostingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.can_post:
            if request.method in ["POST", "PUT", "DELETE"]:
                return HttpResponseForbidden("You are blocked from posting.")
        return self.get_response(request)


class AJAXLoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            not request.user.is_authenticated
            and request.headers.get("x-requested-with") == "XMLHttpRequest"
        ):
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return self.get_response(request)
