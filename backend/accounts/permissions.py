from rest_framework.permissions import BasePermission

class IsSchoolAdmin(BasePermission):
    def has_permission(self, request, view):
        # Ensure user is logged in
        if not request.user or not request.user.is_authenticated:
            return False
        # Then check role
        return getattr(request.user, 'role', None) == 'school_admin'


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, 'role', None) == 'teacher'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, 'role', None) == 'student'


class IsParent(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, 'role', None) == 'parent'

