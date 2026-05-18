from apps.common.permissions import (  # noqa: F401
    IsAuthenticatedAndTenantScoped,
    IsExaminationStaff,
    IsFinanceStaff,
    IsOwner,
    IsRegistrationStaff,
    IsStudent,
    IsTeacher,
    IsUniversityAdmin,
)


class IsTenantOwner(IsAuthenticatedAndTenantScoped):
    """Backward-compatible object-level tenant permission."""
