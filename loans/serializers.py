from rest_framework import serializers
from .models import Loan, UserProfile
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

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'gender', 'dob')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    #profile = serializers.HyperlinkedRelatedField(view_name='userprofile-detail', read_only=True)
    profile = UserProfileSerializer()
    loans = serializers.HyperlinkedRelatedField(many=True, view_name='loan-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'email', 'password', 'is_staff', 'profile', 'loans')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        username = validated_data.get('email')
        user = User.objects.create(username=username, **validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
