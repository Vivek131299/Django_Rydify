from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('location', views.LocationViewSet, basename='location')
# router.register('traveldetails', views.TravelDetailsViewSet, basename='traveldetails')

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.CustomLoginView.as_view(template_name='login_page.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

    path('register_driver/', views.register_driver, name='register_driver'),

    path('traveldetails/', views.TravelDetailsView.as_view(), name='traveldetails'),
    path('delete_traveldetails/<int:pk>/', views.delete_travel_details, name='delete_traveldetails'),
    path('driveravailability/', views.DriverAvailabilityView.as_view(), name='driveravailability'),
    path('delete_driveravailability/<int:pk>/', views.delete_driver_availability, name='delete_driveravailability'),
    path('get_available_drivers_by_travel_detail_id/', views.get_available_drivers_by_travel_detail_id, name='get_available_drivers_by_travel_detail_id'),

    path('', include(router.urls)),
]
