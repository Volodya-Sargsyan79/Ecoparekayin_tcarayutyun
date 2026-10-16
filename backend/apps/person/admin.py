from django.contrib import admin
from django.utils import timezone
from rangefilter.filters import DateRangeFilter
from . import models

admin.site.register(models.Region)
admin.site.register(models.Precinct)
admin.site.register(models.Position)
admin.site.register(models.Car)
admin.site.register(models.UserAccess)

# =========================================================
# ՀԵՐԹԱՓՈԽԵՐ
# =========================================================

@admin.register(models.StationShift)
class StationShiftAdmin(admin.ModelAdmin):
    list_display = (
        "start_shift",
        "end_shift",
        "region",
        "precinct",
        "car",
        "route",
    )

    list_filter = (
        ("start_shift", DateRangeFilter),
        "region",
        "precinct",
    )

    ordering = (
        "-start_shift",
    )

    def formfield_for_foreignkey(
        self,
        db_field,
        request,
        **kwargs,
    ):
        employee_fields = {
            "employee_01",
            "employee_02",
            "employee_03",
            "employee_04",
        }

        object_id = request.resolver_match.kwargs.get("object_id")

        if db_field.name in employee_fields and not object_id:
            kwargs["queryset"] = (
                models.Employee.objects.filter(
                    status=models.Employee.Status.ACTIVE,
                )
                .order_by(
                    "name",
                    "surname",
                )
            )

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs,
        )


# =========================================================
# ԱՇԽԱՏԱԿԻՑՆԵՐ
# =========================================================

@admin.register(models.Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "surname",
        "region",
        "precinct",
        "position",
        "phone",
        "current_camera_number",
        "previous_camera_number",
        "status",
        "status_date",
    )

    search_fields = (
        "name",
        "surname",
        "service_number",
        "phone",
        "camera__number",
        "previous_camera_number",
    )

    ordering = (
        "name",
        "surname",
    )

    list_filter = (
        "status",
        "region",
        "precinct",
        "position",
    )

    actions = (
        "suspend_employees",
        "mark_as_resigned",
        "mark_as_dismissed",
        "mark_as_transferred",
        "restore_employees",
    )

    @admin.display(description="Ընթացիկ տեսախցիկ")
    def current_camera_number(self, obj):
        if obj.camera:
            return obj.camera.number

        return "-"

    def change_employee_status(
        self,
        queryset,
        status,
    ):
        for employee in queryset:
            employee.status = status
            employee.status_date = timezone.localdate()
            employee.save()

    @admin.action(
        description="Կասեցնել ընտրված աշխատակիցների լիազորությունները"
    )
    def suspend_employees(self, request, queryset):
        self.change_employee_status(
            queryset,
            models.Employee.Status.SUSPENDED,
        )

    @admin.action(
        description="Նշել՝ ազատվել է սեփական դիմումի համաձայն"
    )
    def mark_as_resigned(self, request, queryset):
        self.change_employee_status(
            queryset,
            models.Employee.Status.RESIGNED,
        )

    @admin.action(
        description="Նշել՝ ազատվել է աշխատանքից"
    )
    def mark_as_dismissed(self, request, queryset):
        self.change_employee_status(
            queryset,
            models.Employee.Status.DISMISSED,
        )

    @admin.action(
        description="Նշել՝ տեղափոխվել է"
    )
    def mark_as_transferred(self, request, queryset):
        self.change_employee_status(
            queryset,
            models.Employee.Status.TRANSFERRED,
        )

    @admin.action(
        description="Վերականգնել որպես գործող աշխատակից"
    )
    def restore_employees(self, request, queryset):
        queryset.update(
            status=models.Employee.Status.ACTIVE,
            status_date=None,
            status_reason="",
        )

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# =========================================================
# ԵՐԹՈՒՂԻՆԵՐ
# =========================================================

@admin.register(models.Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "region",
        "precinct",
        "route_number",
    )

    ordering = (
        "route_number",
    )

    list_filter = (
        "region",
        "precinct",
    )

# =========================================================
# ՏԵՍԱԽՑԻԿՆԵՐ
# =========================================================

@admin.register(models.Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "region",
        "precinct",
        "assigned_employee",
    )

    search_fields = (
        "number",
        "employee__name",
        "employee__surname",
    )

    list_filter = (
        "region",
        "precinct",
    )

    @admin.display(description="Տրված է աշխատակցին")
    def assigned_employee(self, obj):
        try:
            return obj.employee
        except models.Employee.DoesNotExist:
            return "-"

# =========================================================
# ՀԵՐԹԱՓՈԽԻ ՎԵՐԱԲԵՐՅԱԼ ՏԵՂԵԿՈՒԹՅՈՒՆՆԵՐ
# =========================================================

@admin.register(models.InformationForShift)
class InformationForShiftAdmin(admin.ModelAdmin):
    list_display = (
        "shift",
        "text_info",
        "pdf_file",
    )

    list_filter = (
        ("shift__start_shift", DateRangeFilter),
        "shift__region",
        "shift__precinct",
    )

# =========================================================
# ՕՐՎԱ ՀԵՐԹԱՓՈԽԻ ՓԱՍՏԱԹՂԹԵՐ
# =========================================================

@admin.register(models.ShiftDayInfo)
class ShiftDayInfoAdmin(admin.ModelAdmin):
    list_display = (
        "registration_day",
        "pdf_file",
        "precinct",
    )

    list_filter = (
        ("registration_day", DateRangeFilter),
        "precinct",
    )

# =========================================================
# ԸՆԴՄԻՋՈՒՄՆԵՐ
# =========================================================

@admin.register(models.LunchTime)
class LunchTimeAdmin(admin.ModelAdmin):
    list_display = (
        "start_lanch",
        "end_lanch",
        "formatted_duration",
        "shift",
    )

    readonly_fields = (
        "formatted_duration",
    )

    fields = (
        "start_lanch",
        "end_lanch",
        "formatted_duration",
        "shift",
    )

    list_filter = (
        ("shift__start_shift", DateRangeFilter),
        "shift__region",
        "shift__precinct",
        "shift__car",
    )

    @admin.display(description="Ծախսված ժամանակ")
    def formatted_duration(self, obj):
        if not obj:
            return "00:00"

        return obj.duration_display