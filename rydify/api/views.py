import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .forms import UserRegisterForm, DriverRegisterForm
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Location, TravelDetails, Customer, Driver, DriverAvailability
from .serializers import LocationSerializer, TravelDetailsSerializer
from .forms import TravelDetailsForm, DriverAvailabilityForm
from django.http import QueryDict
from django.views.decorators.csrf import csrf_exempt
from .permissions import IsCustomer, IsDriver
from django.contrib.auth import views as auth_views


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            whatsapp_number = form.cleaned_data.get('whatsapp_number')
            if Customer.objects.filter(whatsapp_number=whatsapp_number).exists():
                messages.error(request, "Whatsapp number already exists")
                return redirect('register')

            form.save()
            user = User.objects.get(username=form.cleaned_data.get('username'))
            customer = Customer(user=user, name=form.cleaned_data.get('first_name') + " " + form.cleaned_data.get('last_name'), whatsapp_number=form.cleaned_data.get('whatsapp_number'))
            customer.save()

            customer_group = Group.objects.get(name='Customers')
            user.groups.add(customer_group)

            messages.success(request, "Registration successful. Now you can login to your account.")
            return redirect('login')

    else:
        form = UserRegisterForm()
        register_driver = DriverRegisterForm()
    return render(request, 'register.html', {'form': form, 'register_driver': register_driver})


def login_page(request):
    if request.method == 'GET':
        return render(request, 'login_page.html')


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    permission_classes = [IsAuthenticated, IsAdminUser]


class TravelDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        form = TravelDetailsForm()
        customer = Customer.objects.filter(user_id=request.user.id).first()
        customer_travel_details = None
        if customer:
            customer_travel_details = TravelDetails.objects.filter(customer_id=customer.id)
        return render(request, "home.html", {'form': form, 'customer': customer, 'customer_travel_details': customer_travel_details})

    def post(self, request):
        customer = Customer.objects.get(user=request.user)
        print(request.data)
        travel_details = TravelDetails.objects.create(date_of_arrival=request.data['date_of_arrival'],
                                                      time_of_arrival=request.data['time_of_arrival'],
                                                      number_of_check_in=request.data['number_of_check_in'],
                                                      pickup=request.data['pickup'],
                                                      drop=request.data['drop'],
                                                      contact=request.data['contact'],
                                                      customer_id=customer.id)
        messages.success(request, "Travel details added.")
        return redirect('traveldetails')


@csrf_exempt
@login_required
def delete_travel_details(request, pk=None):
    if pk:
        travel_details = TravelDetails.objects.get(pk=pk)
        travel_details.delete()
        messages.success(request, "Travel details deleted.")
        return redirect('traveldetails')


class DriverAvailabilityView(APIView):
    permission_classes = [IsAuthenticated, IsDriver]

    def get(self, request):
        form = DriverAvailabilityForm()
        driver = Driver.objects.filter(user_id=request.user.id).first()
        driver_availability_details = None
        if driver:
            driver_availability_details = DriverAvailability.objects.filter(driver_id=driver.id)
        return render(request, "driver_home.html", {'form': form, 'driver': driver, 'driver_availability_details': driver_availability_details})

    def post(self, request):
        driver = Driver.objects.get(user=request.user)
        print(request.data)
        driver_availability = DriverAvailability.objects.create(available_date=request.data['available_date'],
                                                      start_time=request.data['start_time'],
                                                      end_time=request.data['end_time'],
                                                      driver_id=driver.id)
        messages.success(request, "Driver availability details added.")
        return redirect('driveravailability')


@csrf_exempt
@login_required
def delete_driver_availability(request, pk=None):
    if pk:
        driver_availability_details = DriverAvailability.objects.get(pk=pk)
        driver_availability_details.delete()
        messages.success(request, "Driver availability details deleted.")
        return redirect('driveravailability')


def register_driver(request):
    if request.method == 'POST':
        form = DriverRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data.get('username'))
            driver = Driver(user=user, name=form.cleaned_data.get('first_name') + " " + form.cleaned_data.get('last_name'), email=form.cleaned_data.get('email'))
            driver.save()

            driver_group = Group.objects.get(name='Drivers')
            user.groups.add(driver_group)

            messages.success(request, "Registration successful. Now you can login to your account.")
            return redirect('login')

    else:
        form = UserRegisterForm()
        register_driver = DriverRegisterForm()
    return render(request, 'register.html', {'form': form, 'register_driver': register_driver})


class CustomLoginView(auth_views.LoginView):

    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Customers').exists():
            return '/api/traveldetails'
        elif user.groups.filter(name='Drivers').exists():
            return '/api/driveravailability'
        else:
            return '/api/traveldetails'


@csrf_exempt
@login_required
def get_available_drivers_by_travel_detail_id(request):
    print(request.GET.get('travel_detail_id'))
    id = request.GET.get('travel_detail_id')
    travel_details = TravelDetails.objects.get(pk=id)

    availabilities = list(DriverAvailability.objects.filter(available_date=travel_details.date_of_arrival, start_time__lte=travel_details.time_of_arrival, end_time__gte=travel_details.time_of_arrival))
    available_drivers = []
    for a in availabilities:
        available_drivers.append(Driver.objects.get(pk=a.driver_id))

    available_drivers_list = [{'name': driver.name, 'email': driver.email} for driver in available_drivers]

    return JsonResponse(available_drivers_list, safe=False)