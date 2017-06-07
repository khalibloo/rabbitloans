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
        if request.method == 'POST':
            return True
        #Users can view and modify their own accounts
        if request.user == obj:
            return True
        #Only admins can do anything else
        return request.user.is_staff

class LoansPermission(permissions.BasePermission):
    """
    Custom permission for loans.
    """

    def has_permission(self, request, view):
        #Admins cannot create new loans
        if request.user.is_staff and request.method == 'POST':
            return False
        #Users can create new loans
        return True

    def has_object_permission(self, request, view, obj):
        #Admins can only view loans
        if request.user.is_staff:
            return True
        else:
            #Users can create new loans
            # if request.method == 'POST':
            #     return True
            #Users can create new loans and but cannot modify loans
            if request.user == obj.customer:
                if request.method in permissions.SAFE_METHODS:
                    return True
        #Everything else, not allowed
        return False

class LoanSettingsPermission(permissions.BasePermission):
    """
    Custom permission for loans.
    """

    def has_permission(self, request, view):
        #Customers can view the settings
        if request.method == 'GET':
            return True
        #Admins can only edit the settings
        return request.user.is_staff
    def has_object_permission(self, request, view, obj):
        #Customers can view the settings
        if request.method == 'GET':
            return True
        #Admins can only edit the settings
        return request.user.is_staff
