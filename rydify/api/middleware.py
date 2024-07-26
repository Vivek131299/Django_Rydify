from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class RedirectIfUnauthenticatedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated and \
                not request.path.startswith(reverse('login')) and \
                not request.path.startswith(reverse('register')) and \
                not request.path.startswith(reverse('register_driver')) and \
                not request.path.startswith('/admin'):
            return redirect('login')


