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
    #profile = serializers.HyperlinkedRelatedField(view_name='userprofile-detail', read_only=True)
    first_name = serializers.CharField(source='profile.first_name')
    last_name = serializers.CharField(source='profile.last_name')
    gender = serializers.CharField(source='profile.gender')
    dob = serializers.DateField(source='profile.dob')
    loans = serializers.HyperlinkedRelatedField(many=True, view_name='loan-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'email', 'is_staff', 'first_name', 'last_name', 'gender', 'dob', 'loans')


