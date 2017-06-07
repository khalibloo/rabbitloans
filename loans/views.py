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

    # def create(self, request):
    #     settings = LoanSettings.objects.first()
    #     rate = settings.interest_rate
    #     amount = request.data['amount']
        #validate amount
        # if amount < settings.min_amount:
        #     return Response({
        #         'status': 'Bad request',
        #         'message': 'Amount below min allowed.'
        #     }, status=status.HTTP_400_BAD_REQUEST)
        # elif amount > settings.max_amount:
        #     return Response({
        #         'status': 'Bad request',
        #         'message': 'Amount exceeds max allowed.'
        #     }, status=status.HTTP_400_BAD_REQUEST)
        #validate duration
        #duration = request.data['duration']
        # if duration < settings.min_duration:
        #     return Response({
        #         'status': 'Bad request',
        #         'message': 'Duration below min allowed.'
        #     }, status=status.HTTP_400_BAD_REQUEST)
        # elif duration > settings.max_duration:
        #     return Response({
        #         'status': 'Bad request',
        #         'message': 'Duration exceeds max allowed.'
        #     }, status=status.HTTP_400_BAD_REQUEST)
        # collateral = request.data['collateral_worth']
        # #calculate the interest
        # interest = 0
        # cummulativeAmount = amount
        # for i in range(0, duration):
        #     annualInterest = cummulativeAmount * rate
        #     interest += annualInterest
        #     cummulativeAmount += annualInterest
        
        # #get repay amount
        # repay_amount = amount + interest
        # if collateral < repay_amount:
        #     return Response({
        #         'status': 'Bad request',
        #         'message': 'Insufficient collateral.'
        #     }, status=status.HTTP_400_BAD_REQUEST)
        #get date due
        # date_due = addYears(date.today(), duration)

        # serializer = self.serializer_class(data=request.data)
        # if serializer.is_valid():
        #     serializer.save(
        #         customer=self.request.user,
        #         interest_rate=rate,
        #         date_applied=date.today(),
        #         approval_status='P',
        #         repay_amount=amount+interest,
        #         date_due=date_due,
        #         repayment_status='N',
        #         **request.data
        #     )

        #     return Response(
        #         serializer.validated_data, status=status.HTTP_201_CREATED
        #     )

        # return Response({
        #     'status': 'Bad request',
        #     'message': 'Invalid data.'
        # }, status=status.HTTP_400_BAD_REQUEST)

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
    #     return LoanSettings(id=1, **validated_data)

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


def addYears(d, years):
    try:
    #Return same day of the current year        
        return d.replace(year = d.year + years)
    except ValueError:
    #If not same day, it will return other, i.e.  February 29 to March 1 etc.        
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
