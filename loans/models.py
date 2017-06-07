from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Loan(models.Model):
    APPROVAL_STATUS_CHOICES = (
        ('A', 'Approved'),
        ('D', 'Denied'),
        ('P', 'Pending'),
    )
    REPAYMENT_STATUS_CHOICES = (
        ('R', 'Repaid'),
        ('N', 'Not repaid'),
        ('D', 'Defaulted'),
    )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    amount = models.FloatField()
    duration = models.IntegerField()
    interest_rate = models.FloatField()
    collateral_worth = models.FloatField()
    date_applied = models.DateTimeField()
    #approved 'A'| denied 'D'| pending 'P'
    approval_status = models.CharField(default='P', max_length=1, choices=APPROVAL_STATUS_CHOICES)
    date_granted = models.DateTimeField(null=True, blank=True)
    repay_amount = models.FloatField()
    date_due = models.DateTimeField(null=True, blank=True)
    #repaid 'R'| not repaid 'N'| defaulted 'D'
    repayment_status = models.CharField(default='N', max_length=1, choices=REPAYMENT_STATUS_CHOICES)
    date_repaid = models.DateTimeField(null=True, blank=True)

class LoanSettings(models.Model):
    min_amount = models.FloatField()
    max_amount = models.FloatField()
    min_duration = models.IntegerField()
    max_duration = models.IntegerField()
    interest_rate = models.FloatField()

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField()

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)