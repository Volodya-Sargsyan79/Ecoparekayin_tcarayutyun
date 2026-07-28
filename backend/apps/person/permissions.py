from rest_framework.permissions import BasePermission

class GroupPermission(BasePermission):
    allowed_groups = []
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.groups.filter(
            name__in=self.allowed_groups
        ).exists()

class IsAdmin(GroupPermission):
    allowed_groups = ["Ադմիններ"]

class IsOperator(GroupPermission):
    allowed_groups = ["Օպերատորներ"]

class IsDutyOfficer(GroupPermission):
    allowed_groups = ["Հերթապահներ"]

class IsPrecinctHead(GroupPermission):
    allowed_groups = ["Տեղամասի պետեր"]

class IsRegionHead(GroupPermission):
    allowed_groups = ["Վարչության պետեր"]

class IsForShiftAdd(GroupPermission):
    allowed_groups = ["Ադմիններ", "Օպերատորներ", "Հերթապահներ"]

class IsForShiftInformationsAdd(GroupPermission):
    allowed_groups = ["Հերթապահներ", "Տեղամասի պետեր", "Վարչության պետեր"]

class IsForEmployee(GroupPermission):
    allowed_groups = ["Ադմիններ", "Օպերատորներ", "Տեղամասի պետեր", "Վարչության պետեր"]

class IsAllUsers(GroupPermission):
    allowed_groups = ["Ադմիններ", "Օպերատորներ", "Հերթապահներ", "Տեղամասի պետեր", "Վարչության պետեր"]