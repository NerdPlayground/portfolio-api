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

    def get(self, request, *args, **kwargs):
        """
        Lists all registers users. 
        Only available to admins
        """

        return super().get(request, *args, **kwargs)

class UserDetail(generics.RetrieveAPIView):
    lookup_field='username'
    queryset=get_user_model().objects.all()
    serializer_class=UserSerializer
    
    def get(self, request, *args, **kwargs):
        """
        Retrieves a user with the given username. 
        Available to authenticated and unauthenticated users.
        """

        return super().get(request, *args, **kwargs)

class CurrentUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Retrieves the information of the current authenticated user"""

        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """Allows the current authenticated user to update their information"""

        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """Allows the current authenticated user to update their information"""

        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """Allows the current authenticated user to delete their information"""

        return super().delete(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)
    
    @extend_schema(
        responses=None,
        request=LoginSerializer,
    )
    def post(self, request, format=None):
        """
        Authenticates user and returns a token. 
        The token is valid for 24 hours
        """

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
        """
        Logs out user from current client session and  
        invalidates the token supplied during authentication
        """
        
        return super().post(request,format)

class LogoutAllView(KnoxLogoutAllView):
    @extend_schema(
        request=None,
        responses=None,
    )
    def post(self, request, format=None):
        return super().post(request,format)