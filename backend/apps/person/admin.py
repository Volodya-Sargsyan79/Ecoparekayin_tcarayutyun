from django.contrib import admin
from . import models

admin.site.register(models.Region)
admin.site.register(models.Precinct)
admin.site.register(models.Position)
admin.site.register(models.Car)
admin.site.register(models.Employee)
admin.site.register(models.StationShift)
admin.site.register(models.Route)
admin.site.register(models.UserAccess)
admin.site.register(models.InformationForShift)
admin.site.register(models.LunchTime)

