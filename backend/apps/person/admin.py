from django.contrib import admin
from . import models

admin.site.register(models.Region)
admin.site.register(models.Precinct)
admin.site.register(models.Position)
admin.site.register(models.Car)
admin.site.register(models.StationShift)
admin.site.register(models.UserAccess)
admin.site.register(models.InformationForShift)
admin.site.register(models.LunchTime)
admin.site.register(models.Camera)
admin.site.register(models.ShiftDayInfo)

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'surname',
        'region',
        'precinct',
        'position',
        'phone',
    )

    ordering = ('name',)

    list_filter = (
        'region',
        'precinct',
        'position',
    )


@admin.register(models.Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        'region',
        'precinct',
        'route_number',
    )
    
    ordering = ('route_number',)

    list_filter = (
        'region',
        'precinct'
    )