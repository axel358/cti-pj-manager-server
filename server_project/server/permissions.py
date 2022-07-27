from rest_framework import permissions


# Future functionality class
class IsHumanResources(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='human_resources'):
            return bool(request.user)


class IsProgramChief(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='program_chiefs'):
            return bool(request.user)


class IsProjectChief(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='project_chiefs'):
            return bool(request.user)


class IsEconomyChief(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='economy'):
            return bool(request.user)


class IsVicedChief(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='vicedec_inv_postgr'):
            return bool(request.user)
