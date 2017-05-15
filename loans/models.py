from django.db import models
from django.contrib.auth.models import User


class Loan (models.Model):
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
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    duration = models.IntegerField()
    interest_rate = models.FloatField()
    collateral_worth = models.FloatField()
    date_applied = models.DateTimeField()
    #approved 'A', denied 'D', pending 'P'
    approval_status = models.CharField(default='P', max_length=1, choices=APPROVAL_STATUS_CHOICES)
    date_granted = models.DateTimeField(blank=True)
    repay_amount = models.FloatField()
    date_due = models.DateTimeField(blank=True)
    #repaid 'R', not repaid 'N', defaulted 'D'
    repayment_status = models.CharField(default='N', max_length=1, choices=REPAYMENT_STATUS_CHOICES)
    date_repaid = models.DateTimeField(blank=True)
