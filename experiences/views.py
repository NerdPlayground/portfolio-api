from .models import Experience
from pocket.views import project_status
from .serializers import ExperienceSerializer
from rest_framework import generics,permissions
from profiles.permissions import isOwnerOrReadOnly

class Experiences(generics.ListAPIView):
    """
    Lists all the experiences of all registered users. 
    Only available to admin users.
    """

    queryset=Experience.objects.all()
    serializer_class=ExperienceSerializer
    permission_classes=[permissions.IsAdminUser]

class ExperienceList(generics.ListCreateAPIView):
    serializer_class=ExperienceSerializer
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Allows an authenticated user to add an experience."""

        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """Lists all the authenticated user's experiences."""

        return super().get(request, *args, **kwargs)

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

    def get(self, request, *args, **kwargs):
        """
        Retrieves an experience. 
        Only available to authenticated users.
        """

        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """
        Retrieves an experience to update. 
        Only available to the owner of the experience.
        """

        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """
        Retrieves an experience to update. 
        Only available to the owner of the experience.
        """

        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """
        Retrieves an experience to delete. 
        Only available to the owner of the experience.
        """
        
        return super().delete(request, *args, **kwargs)

    def perform_update(self,serializer):
        ongoing,end_date=project_status(self.request)
        serializer.save(
            ongoing=ongoing,end_date=end_date
        )