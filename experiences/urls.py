from .views import *
from django.urls import path

urlpatterns=[
    path("",ExperienceList.as_view(),name="experience-list"),
    path("all/",Experiences.as_view(),name="all-experiences"),
    path("<str:pk>/",ExperienceDetail.as_view(),name="experience-detail"),
]