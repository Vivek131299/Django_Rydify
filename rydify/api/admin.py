from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Customer)
admin.site.register(models.Driver)
admin.site.register(models.TravelDetails)
admin.site.register(models.DriverAvailability)
admin.site.register(models.Location)
