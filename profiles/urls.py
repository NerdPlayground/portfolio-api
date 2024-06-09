from .views import *
from django.urls import path

urlpatterns=[
    path("",UserList.as_view(),name="user-list"),
    path("<str:username>/",UserDetail.as_view(),name="user-detail"),
]