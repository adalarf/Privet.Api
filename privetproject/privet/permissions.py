from rest_framework.permissions import BasePermission
from .models import Buddy


class IsStudentUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_student)


class IsBuddyUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_buddy)


class IsTeamleadUser(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_teamlead)



class IsConfirmedBuddyUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_buddy:
            buddy = Buddy.objects.get(user=request.user)
            return buddy.buddy_status
        return False