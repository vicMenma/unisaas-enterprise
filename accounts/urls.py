from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import TenantTokenObtainPairView

urlpatterns = [
    path('auth/login', TenantTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
