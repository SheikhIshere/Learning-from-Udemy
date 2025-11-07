from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """allow user to  edit their own profile only"""

    def has_object_permission(self, request, view, obj):
        """check user is trying to change his/her user profile or not"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
    
class UpdateOwnStatus(permissions.BasePermission):
    """Allow User update their own profile only"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id