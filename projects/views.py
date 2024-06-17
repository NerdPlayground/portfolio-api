from .models import Project
from pocket.views import project_status
from .serializers import ProjectSerializer
from rest_framework import generics,permissions
from profiles.permissions import isOwnerOrReadOnly

class Projects(generics.ListAPIView):
    """
    Lists all the projects of all registered users. 
    Only available to admin users
    """

    queryset=Project.objects.all()
    serializer_class=ProjectSerializer
    permission_classes=[permissions.IsAdminUser]

class ProjectsList(generics.ListCreateAPIView):
    serializer_class=ProjectSerializer
    permission_classes=[permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Allows a logged in user to add a project."""

        return super().post(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        """Lists all the logged in user's projects."""

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

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

    def get(self, request, *args, **kwargs):
        """
        Retrieves a project. 
        Only available to logged in users.
        """

        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """
        Retrieves a project to update. 
        Only available to the owner of the project.
        """

        return super().put(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        """
        Retrieves a project to update. 
        Only available to the owner of the project.
        """
        
        return super().patch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        """
        Retrieves a project to delete. 
        Only available to the owner of the project.
        """
        
        return super().delete(request, *args, **kwargs)

    def perform_update(self,serializer):
        ongoing,end_date=project_status(self.request)
        serializer.save(
            ongoing=ongoing,end_date=end_date
        )