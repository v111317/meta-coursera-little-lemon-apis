from rest_framework import permissions

class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.groups.filter(name="Delivery Crew").exists():
            return True
        return False
    
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.groups.filter(name="Manager").exists():
            return True
        return False