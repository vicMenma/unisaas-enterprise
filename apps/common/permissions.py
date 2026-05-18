from rest_framework import permissions


def has_tenant_access(request):
    tenant = getattr(request, "tenant", None)
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    return tenant is not None and str(user.university_id) == str(tenant.id)


class IsAuthenticatedAndTenantScoped(permissions.BasePermission):
    message = "Authenticated user is not scoped to the resolved tenant."

    def has_permission(self, request, view):
        return has_tenant_access(request)

    def has_object_permission(self, request, view, obj):
        university_id = getattr(obj, "university_id", None)
        if university_id is None:
            return has_tenant_access(request)
        return has_tenant_access(request) and str(university_id) == str(request.tenant.id)


class RolePermission(IsAuthenticatedAndTenantScoped):
    allowed_roles = ()

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.is_superuser or request.user.role in self.allowed_roles


class IsOwner(RolePermission):
    allowed_roles = ("owner",)


class IsUniversityAdmin(RolePermission):
    allowed_roles = ("owner", "university_admin")


class IsRegistrationStaff(RolePermission):
    allowed_roles = ("owner", "university_admin", "registration")


class IsExaminationStaff(RolePermission):
    allowed_roles = ("owner", "university_admin", "examination", "teacher")


class IsFinanceStaff(RolePermission):
    allowed_roles = ("owner", "university_admin", "registration")


class IsTeacher(RolePermission):
    allowed_roles = ("teacher",)


class IsStudent(RolePermission):
    allowed_roles = ("student",)
