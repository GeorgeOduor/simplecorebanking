import datetime
from django.db import models

# Create your models here.
class UserAccount(models.Model):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    mobile     = models.CharField(max_length=50,unique=True)
    nationalid = models.CharField(max_length=50,unique=True)
    gender     = models.CharField(max_length=50, choices=[
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    ])
    dob        = models.DateField()
    accountid  = models.CharField(max_length=50,unique=True)
    # address details
    zip_code   = models.CharField(max_length=50)
    address    = models.CharField(max_length=50)
    city       = models.CharField(max_length=50)
    country    = models.CharField(max_length=50)
    status     = models.CharField(max_length=50, choices=[
        ('ACTIVE', 'ACTIVE'),
        ('BLOCKED', 'BLOCKED'),
        ('SUSPENDED', 'SUSPENDED')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    
    class Meta:
        ordering = ['-created_at']

class Transactions(models.Model):
    client = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    transaction_type        = models.CharField(max_length=50, choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')])
    transaction_date        = models.DateTimeField(auto_now_add=True,null=False,)
    transaction_amount      = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_balance     = models.DecimalField(max_digits=10, decimal_places=2)
    # transaction_description = models.CharField(max_length=50)
    created_at              = models.DateTimeField(auto_now_add=True,)
    modified_at             = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.transaction_type
    
    class Meta:
        ordering = ['-transaction_date']





