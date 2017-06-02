from rest_framework.decorators import detail_route
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Loan, UserProfile
from .serializers import LoanSerializer, UserSerializer
from .permissions import IsOwner, CreationAllowed
from django.contrib.auth.models import User


class LoanViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = ([permissions.IsAuthenticated, IsOwner, permissions.IsAdminUser,])

    #@detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    #def highlight(self, request, *args, **kwargs):
    #    snippet = self.get_object()
    #    return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    
    serializer_class = UserSerializer
    permission_classes = ([permissions.IsAuthenticated, CreationAllowed])

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
    
    #@detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    @detail_route()
    def me(self, request, *args, **kwargs):
        me = self.get_object()
        return Response(request.user)

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
        #me = self.get_object()
        return Response(request.user)


