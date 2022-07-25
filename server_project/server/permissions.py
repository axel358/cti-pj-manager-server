from rest_framework import permissions


# Future functionality class
class IsHumanResources(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='human_res'):
            return bool(request.user)
