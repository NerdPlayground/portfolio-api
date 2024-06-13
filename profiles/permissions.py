from rest_framework import permissions

class isOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        # Read permissions to any request
        if request.method in permissions.SAFE_METHODS: return True

        # Write permissions to object owners
        return obj.user==request.user