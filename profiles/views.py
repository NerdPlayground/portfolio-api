from django.contrib.auth import get_user_model
from rest_framework import generics,permissions
from .models import Profile
from .permissions import *
from .serializers import ProfileSerializer,UserSerializer

class UserList(generics.ListAPIView):
    queryset=get_user_model().objects.all()
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAdminUser]

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field='username'
    queryset=get_user_model().objects.all()
    serializer_class=UserSerializer
    permission_classes=[isUserOrReadOnly]