from .views import *
from django.urls import path

urlpatterns=[
    path("",ProjectsList.as_view(),name="project-list"),
    path("all/",Projects.as_view(),name="all-projects"),
    path("<str:pk>/",ProjectDetail.as_view(),name="project-detail"),
]