from rest_framework.decorators import detail_route
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import IntegrityError
from .models import Loan, LoanSettings, UserProfile
from .serializers import LoanSerializer, LoanSettingsSerializer, UserSerializer
from .permissions import IsOwner, CreationAllowed, LoansPermission, LoanSettingsPermission
from django.contrib.auth.models import User

from datetime import date

class LoanViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = ([permissions.IsAuthenticated, LoansPermission,])

    #@detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    #def highlight(self, request, *args, **kwargs):
    #    snippet = self.get_object()
    #    return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class LoanSettingsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = LoanSettings.objects.all()
    serializer_class = LoanSettingsSerializer
    permission_classes = ([permissions.IsAuthenticated, LoanSettingsPermission,])

    # def create(self, validated_data):
    #     # settings = LoanSettings.objects.first()
    #     # if settings is not None:
    #     #    return settings
    #     return LoanSettings.objects.create(id=1, **validated_data)

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    
    serializer_class = UserSerializer
    permission_classes = ([CreationAllowed])

    def get_queryset(self):
        """
        This view should return a list of all the users if we're admin.
        Otherwise, only the current user is returned.
        """
        user = self.request.user
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(username=self.request.user.username)

    def create(self, request, *args, **kwargs):
        try:
            return super(viewsets.ModelViewSet, self).create(request, *args, **kwargs)
        except IntegrityError:
            content = {'error': 'IntegrityError'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    

class MeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    
    serializer_class = UserSerializer
    permission_classes = ([permissions.IsAuthenticated])

    def get_queryset(self):
        """
        This view should return a list of all the users if we're admin.
        Otherwise, only the current user is returned.
        """
        return User.objects.filter(username=self.request.user.username)
            
    def retrieve(self, request, *args, **kwargs):
        return Response(request.user)

