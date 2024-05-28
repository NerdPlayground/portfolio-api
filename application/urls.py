"""
URL configuration for application project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.urls.conf import re_path
from allauth.account.views import ConfirmEmailView
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # password/reset, password/reset/confirm, password/reset/validate_token
    path("api/v1/dj-rest-auth/password/reset/", include('django_rest_passwordreset.urls', namespace='password_reset')),
    # /user, /login, /logout, /password/change, /password/reset/, /password/reset/confirm/
    path("api/v1/dj-rest-auth/", include("dj_rest_auth.urls")),
    # account-confirm-email/
    re_path('api/v1/dj-rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),name='account_confirm_email'),
    # verify-email/ resend-email/ account-email-verification-sent/
    path("api/v1/dj-rest-auth/registration/",include("dj_rest_auth.registration.urls")),
    path("users/",include("profiles.urls")),
    path("projects/",include("projects.urls")),
    path("experiences/",include("experiences.urls")),
    # path("",include(".urls")),
]