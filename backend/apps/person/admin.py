from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.RegionArmenia)
admin.site.register(models.Cities)
admin.site.register(models.Villages)
admin.site.register(models.Region)
admin.site.register(models.Precinct)
admin.site.register(models.Position)
admin.site.register(models.Employee)
admin.site.register(models.Citizen)
admin.site.register(models.InfoAboutFire)
admin.site.register(models.StartCallDate)
admin.site.register(models.OperationalControlCenter)
# @admin.register(models.Employee) 
# class EmployeeAdmin(admin.ModelAdmin):
#     list_display = ("name", "surname", "region", "precinct", "position")

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "precinct":
#             from .models import Precinct, Employee

#             obj_id = request.resolver_match.kwargs.get("object_id")
#             if obj_id:
#                 try:
#                     emp = Employee.objects.get(pk=obj_id)
#                     region = emp.region

#                     precincts_in_region = Precinct.objects.filter(region=region)

#                     print(f"All precincts in region '{region}':")
#                     for p in precincts_in_region:
#                         print(f"- {p}")  # uses __str__()

#                     kwargs["queryset"] = precincts_in_region

#                 except Employee.DoesNotExist:
#                     kwargs["queryset"] = Precinct.objects.none()
#             else:
#                 kwargs["queryset"] = Precinct.objects.none()

#         return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
