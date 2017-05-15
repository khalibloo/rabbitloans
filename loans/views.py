from rest_framework.decorators import detail_route
from rest_framework import viewsets, permissions
from .models import Loan
from .serializers import LoanSerializer, UserSerializer
from .permissions import IsOwner
from django.contrib.auth.models import User


class LoanViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = ([IsOwner, permissions.IsAdminUser,])

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
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ([permissions.IsAdminUser,])