from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a loan object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the loan or admins.
        return obj.customer == request.user

class CreationAllowed(permissions.BasePermission):
    """
    Custom permission to only allow anyone to signup.
    """

    def has_object_permission(self, request, view, obj):
        #Anyone can create a user account
        if request.method == 'PUT':
            return True
        #Users can view and modify their own accounts
        if request.user == obj:
            return True
        #Only admins can do anything else
        return request.user.is_staff