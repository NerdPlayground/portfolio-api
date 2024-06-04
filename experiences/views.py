from .models import Experience
from pocket.views import project_status
from .serializers import ExperienceSerializer
from rest_framework import generics,permissions
from profiles.permissions import isOwnerOrReadOnly

class Experiences(generics.ListAPIView):
    queryset=Experience.objects.all()
    serializer_class=ExperienceSerializer
    permission_classes=[permissions.IsAdminUser]

class ExperienceList(generics.ListCreateAPIView):
    serializer_class=ExperienceSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Experience.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        ongoing,end_date=project_status(self.request)
        serializer.save(
            user=self.request.user,
            ongoing=ongoing,end_date=end_date
        )

class ExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=Experience.objects.all()
    serializer_class=ExperienceSerializer
    permission_classes=[permissions.IsAuthenticated,isOwnerOrReadOnly]

    def perform_update(self,serializer):
        ongoing,end_date=project_status(self.request)
        serializer.save(
            ongoing=ongoing,end_date=end_date
        )