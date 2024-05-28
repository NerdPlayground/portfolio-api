from .models import Project
from pocket.views import project_status
from .serializers import ProjectSerializer
from rest_framework import generics,permissions
from profiles.permissions import isOwnerOrReadOnly

class ProjectsList(generics.ListCreateAPIView):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self,serializer):
        ongoing,end_date=project_status(self.request)
        serializer.save(
            user=self.request.user,
            ongoing=ongoing,end_date=end_date
        )

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Project.objects.all()
    serializer_class=ProjectSerializer
    permission_classes=[permissions.IsAuthenticated,isOwnerOrReadOnly]

    def perform_update(self,serializer):
        ongoing,end_date=project_status(self.request)
        serializer.save(
            ongoing=ongoing,end_date=end_date
        )