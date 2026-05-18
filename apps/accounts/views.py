from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.common.permissions import IsAuthenticatedAndTenantScoped

from .serializers import TenantTokenObtainPairSerializer, UserProfileSerializer


class TenantTokenObtainPairView(TokenObtainPairView):
    serializer_class = TenantTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticatedAndTenantScoped]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)
