from .views import *
from django.urls import path

urlpatterns=[
    path("",ExperienceList.as_view(),name="experience-list"),
    path("<str:pk>/",ExperienceDetail.as_view(),name="experience-detail"),
]