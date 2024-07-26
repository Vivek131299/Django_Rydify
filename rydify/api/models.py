from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    whatsapp_number = models.CharField(max_length=20)


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)


class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class TravelDetails(models.Model):
    customer = models.ForeignKey(Customer, related_name='travel_details', on_delete=models.CASCADE)
    date_of_arrival = models.DateField()
    time_of_arrival = models.TimeField()
    number_of_check_in = models.IntegerField(default=1)
    pickup = models.CharField(max_length=200)
    drop = models.CharField(max_length=200)
    contact = models.CharField(max_length=100)


class DriverAvailability(models.Model):
    driver = models.ForeignKey(Driver, related_name='driver_availability', on_delete=models.CASCADE)
    available_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


