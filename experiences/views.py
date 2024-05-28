from .models import Experience
from pocket.views import project_status
from .serializers import ExperienceSerializer
from rest_framework import generics,permissions
from profiles.permissions import isUserOrReadOnly

class ExperienceList(generics.ListCreateAPIView):
    queryset=Experience.objects.all()
    serializer_class=ExperienceSerializer
    permissions_classes=[permissions.IsAuthenticated]

    def perform_create(self,serializer):
        ongoing,end_date=project_status(self.request)
        serializer.save(
            user=self.request.user,
            ongoing=ongoing,end_date=end_date
        )

class ExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Experience.objects.all()
    serializer_class=ExperienceSerializer
    permissions_classes=[permissions.IsAuthenticated,isUserOrReadOnly]

    def perform_update(self,serializer):
        ongoing,end_date=project_status(self.request)
        serializer.save(
            ongoing=ongoing,end_date=end_date
        )