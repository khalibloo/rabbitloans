from rest_framework import serializers
from .models import Loan, LoanSettings, UserProfile
from django.contrib.auth.models import User
from datetime import date

class LoanSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.username')
    customer_fname = serializers.ReadOnlyField(source='customer.profile.first_name')
    customer_lname = serializers.ReadOnlyField(source='customer.profile.last_name')
    class Meta:
        model = Loan
        fields = (
            'id',
            'customer',
            'customer_fname',
            'customer_lname',
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
        extra_kwargs = {
            'interest_rate': {'required': False},
            'date_applied': {'required': False},
            'repay_amount': {'required': False},
        }
    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        settings = LoanSettings.objects.first()
        rate = settings.interest_rate

        #if loan is being updated by admin using PATCH
        if (self.context['request'].method == 'PATCH'):
            return data
        #validate amount
        amount = data['amount']
        if amount < settings.min_amount:
            raise serializers.ValidationError("amount below minimum allowed")
        elif amount > settings.max_amount:
            raise serializers.ValidationError("amount exceeds maximum allowed")
        #validate duration
        duration = data['duration']
        if duration < settings.min_duration:
            raise serializers.ValidationError("duration below minimum allowed")
        elif duration > settings.max_duration:
            raise serializers.ValidationError("duration exceeds maximum allowed")
        
        collateral = data['collateral_worth']
        interest = self.getInterest(amount, duration, rate)
        
        #get repay amount
        repay_amount = amount + interest
        if collateral < repay_amount:
            raise serializers.ValidationError("insufficient collateral")
        return data

    def create(self, validated_data):
        settings = LoanSettings.objects.first()
        amount = validated_data['amount']
        duration = validated_data['duration']
        rate = settings.interest_rate
        repay_amount = amount + self.getInterest(amount, duration, rate)
        
        return Loan.objects.create(
            customer=validated_data['customer'],
            amount=amount,
            duration=duration,
            interest_rate=rate,
            collateral_worth=validated_data['collateral_worth'],
            repay_amount=repay_amount,
            date_applied=date.today(),
            date_due=addYears(date.today(), duration),
            approval_status='P',
            repayment_status='N'
            #**validated_data
        )

    def getInterest(self, amount, duration, rate):
        interest = 0
        cummulativeAmount = amount
        for i in range(0, duration):
            annualInterest = cummulativeAmount * rate
            interest += annualInterest
            cummulativeAmount += annualInterest
        return interest

class LoanSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanSettings
        fields = ('min_amount', 'max_amount', 'min_duration', 'max_duration', 'interest_rate')

    def create(self, validated_data):
        settings = LoanSettings.objects.first()
        if settings is None:
            settings = LoanSettings(**validated_data)
        return settings

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'gender', 'dob')

class UserSerializer(serializers.ModelSerializer):
    #profile = serializers.HyperlinkedRelatedField(view_name='userprofile-detail', read_only=True)
    profile = UserProfileSerializer()
    loans = LoanSerializer(many=True, read_only=True)

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

def addYears(d, years):
    try:
    #Return same day of the current year        
        return d.replace(year = d.year + years)
    except ValueError:
    #If not same day, it will return other, i.e.  February 29 to March 1 etc.        
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
