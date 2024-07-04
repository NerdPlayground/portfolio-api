from django.urls import path
from .views import (
    UserList,UserDetail,
    UserProjectList,UserExperienceList
)

urlpatterns=[
    path("",UserList.as_view(),name="user-list"),
    path("<str:username>/",UserDetail.as_view(),name="user-detail"),
    path("<str:username>/projects/",UserProjectList.as_view(),name="user-projects"),
    path("<str:username>/experiences/",UserExperienceList.as_view(),name="user-experiences"),
]