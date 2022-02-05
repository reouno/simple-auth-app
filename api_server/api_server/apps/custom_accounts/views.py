from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_spectacular.utils import extend_schema
from rest_framework import status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api_server.apps.custom_accounts import models, serializers


class SetCsrf(APIView):
    """Set-CSRF view"""

    @extend_schema(
        responses=serializers.MessageSerializer,
    )
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return Response(serializers.MessageSerializer({'message': 'CSRF cookie set'}).data,
                        status=status.HTTP_200_OK)


class AuthenticationRequired:
    """Base class for view that require authentication"""
    permission_classes = [IsAuthenticated]


class HelloView(APIView):
    """Hello view just return 'Hello.'"""

    @extend_schema(
        responses=serializers.MessageSerializer,
    )
    def get(self, _request):
        """Just return Hello."""
        return Response(serializers.MessageSerializer({'message': 'Hello.'}).data,
                        status=status.HTTP_200_OK)


class Login(APIView):
    """Login view"""

    @extend_schema(
        request=serializers.NativeLoginSerializer,
        responses=serializers.UserSerializer,
    )
    def post(self, request):
        """Login."""
        serializer = serializers.NativeLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'errors': {'__all__': 'Please enter both username and password'}},
                            status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=serializer.validated_data['email'],
                            password=serializer.validated_data['password'])
        if user is not None:
            user_detail: models.CustomUser = models.CustomUser.objects.get_by_natural_key(
                username=user)
            login(request, user)
            return Response(serializers.UserSerializer(user_detail).data,
                            status=status.HTTP_200_OK)

        return Response({
            'detail': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


class Logout(AuthenticationRequired, APIView):
    """Logout view"""

    @extend_schema(
        responses=serializers.MessageSerializer,
    )
    def post(self, request):
        """Logout from current session."""
        logout(request)
        return Response(serializers.MessageSerializer({'message': 'Logged out'}).data)


class UserViewSet(AuthenticationRequired,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """Get information of the current user"""
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user
