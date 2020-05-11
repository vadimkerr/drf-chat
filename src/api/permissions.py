from rest_framework import permissions


class IsSenderOrReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.sender == request.user or obj.receiver == request.user
        else:
            return obj.sender == request.user
