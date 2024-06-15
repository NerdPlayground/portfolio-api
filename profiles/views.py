from .permissions import *
from drf_spectacular.utils import extend_schema
from rest_framework import generics,permissions
from django.contrib.auth import login,get_user_model
from .serializers import UserSerializer,LoginSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import (
    LoginView as KnoxLoginView,
    LogoutView as KnoxLogoutView,
    LogoutAllView as KnoxLogoutAllView,
)

class UserList(generics.ListAPIView):
    queryset=get_user_model().objects.all()
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAdminUser]

class UserDetail(generics.RetrieveAPIView):
    lookup_field='username'
    queryset=get_user_model().objects.all()
    serializer_class=UserSerializer

class CurrentUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    @extend_schema(
        responses=None,
        request=LoginSerializer,
    )
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)

class LogoutView(KnoxLogoutView):
    @extend_schema(
        request=None,
        responses=None,
    )
    def post(self, request, format=None):
        return super().post(request,format)

class LogoutAllView(KnoxLogoutAllView):
    @extend_schema(
        request=None,
        responses=None,
    )
    def post(self, request, format=None):
        return super().post(request,format)