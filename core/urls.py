from django.urls import path

from .views import *

app_name = 'core'

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('accounts/', AccountsListing.as_view(), name='accounts'),
    path('create_account/', CreateNewAccount.as_view(), name='create_account'),
    path('accounts/delete/<str:account_id>/', DeleteAccount.as_view(), name='delete_account'),
    path('accounts/activate/<str:account_id>/', ActivateAccount.as_view(), name='activate_account'),
    path('accounts/suspend/<str:account_id>/', SuspendAccount.as_view(), name='suspend_account'),
    path('accounts/block/<str:account_id>/', BlockAccount.as_view(), name='block_account'),
    path('accounts/<str:account_id>/', AccountDetails.as_view(), name='account_details'),
    path('transactions/', TransactionsListing.as_view(), name='transactions'),
    path('transactions/deposit/', CreateDeposit.as_view(), name='create_deposit'),
    path('transactions/withdraw/', CreateWithdraw.as_view(), name='create_withdraw'),
    path('transactions/transfer_funds/', AccountTransfer.as_view(), name='transfer_funds'),
]