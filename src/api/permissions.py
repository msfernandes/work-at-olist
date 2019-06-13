from rest_framework import permissions


class GetAndPostOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method.lower() in ['get', 'post']
