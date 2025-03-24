from django.http import HttpResponseForbidden


class BlockPostingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.can_post:
            if request.method in ["POST", "PUT", "DELETE"]:
                return HttpResponseForbidden("You are blocked from posting.")
        return self.get_response(request)
