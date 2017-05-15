from rest_framework import serializers
from .models import Loan
from django.contrib.auth.models import User

class LoanSerializer(serializers.HyperlinkedModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')
    class Meta:
        model = Loan
        fields = (
            'id',
            'customer',
            'amount',
            'duration',
            'interest_rate',
            'collateral_worth',
            'date_applied',
            'approval_status',
            'date_granted',
            'repay_amount',
            'date_due',
            'repayment_status',
            'date_repaid',
        )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    loans = serializers.HyperlinkedRelatedField(many=True, view_name='loan-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'loans')

