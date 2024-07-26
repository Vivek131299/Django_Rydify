from rest_framework.views import exception_handler
from django.shortcuts import render


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    # Check if the exception is a permission denied error
    if response is not None and response.status_code == 403:
        request = context['request']
        print(request.path)
        redirect_url = 'driveravailability'
        if 'driveravailability' in request.path:
            redirect_url = 'traveldetails'
        return render(request, 'custom_403.html', {'redirect_url': redirect_url}, status=403)