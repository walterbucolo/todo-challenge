from rest_framework import permissions
from todolist.models import Task


class IsOwnerPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an task to access it.
    """

    def has_permission(self, request, view):
        authenticated_user = request.user.id
        requested_user = view.kwargs.get('pk')
        
        return authenticated_user == requested_user

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Task):
            obj = obj.user
        
        return obj == request.user
    