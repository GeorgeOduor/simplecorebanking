from django.contrib import admin
from .models import UserAccount,Transactions
# Register your models here.

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'mobile', 'nationalid', 'gender', 'dob', 'accountid', 'zip_code', 'address', 'city', 'country', 'created_at', 'modified_at']
    
@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['client', 'transaction_type', 'transaction_date', 'transaction_amount', 'transaction_balance', 'created_at']

