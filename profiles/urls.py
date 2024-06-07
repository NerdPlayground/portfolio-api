from .views import *
from django.urls import path
from .views import LoginView
from knox import views as knox_views

urlpatterns=[
    path("",UserList.as_view(),name="user-list"),
    path("login/", LoginView.as_view(), name='knox_login'),
    path("logout/", knox_views.LogoutView.as_view(), name='knox_logout'),
    path("logout/all/", knox_views.LogoutAllView.as_view(), name='knox_logout_all'),
    path("<str:username>/",UserDetail.as_view(),name="user-detail"),
]