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


class IsConfirmedBuddyArrivalUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_buddy:
            buddy = request.user.buddy
            confirmed_arrival = buddy.buddy_arrivals.filter(student=view.get_object(), buddy_arrival_status=True).first()
            return confirmed_arrival is not None
        return False