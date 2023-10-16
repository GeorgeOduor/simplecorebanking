from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.shortcuts import redirect
from django.contrib import messages
from .scripts.create_accs import generate_account_id,new_trx_balance,check_balance
# Create your views here.
from .models import *

class Home(View):
    accounts = UserAccount.objects.all()
    transactions = Transactions.objects.all()
    def get(self, request):
        
        context = {
            'title': 'Home',
            'total_clients' : self.accounts.count(),
        'total_transactions' : self.transactions.count(),
        'total_debits' : self.transactions.filter(transaction_type='DEBIT').count(),
        'total_credits' : self.transactions.filter(transaction_type='CREDIT').count()
            }
        
        return render(request, 'core/home.html', context)
    
class AccountsListing(View):
    model = UserAccount
    template_name = 'core/accounts.html'

    def get(self, request):

        context = {
            'title': 'Accounts Listing',
            'accounts': UserAccount.objects.all()
            }
        return render(request, 'core/accounts.html', context)
    

class CreateNewAccount(View):

    def get(self, request):
        
        context = {
            'title': 'Create New Account'
            }
        return render(request, 'core/create-account.html', context)
    
    def post(self, request):
        accounts_info = request.POST
        first_name = accounts_info.get('first_name')
        last_name = accounts_info.get('last_name')
        email = accounts_info.get('email')
        mobile = accounts_info.get('mobile')
        nationalid = accounts_info.get('nationalid')
        gender = accounts_info.get('gender')
        dob = accounts_info.get('dob')
        zip_code = accounts_info.get('zip_code')
        address = accounts_info.get('address')
        city = accounts_info.get('city')
        country = accounts_info.get('country')
        status = accounts_info.get('status')
        # account_id = generate_account_id( prefix = "001901", model = UserAccount, id_field = 'id' )
        try:
            account_id = generate_account_id( prefix = "001901", model = UserAccount, id_field = 'accountid' )
            UserAccount.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                nationalid=nationalid,
                gender=gender,
                dob=dob,
                accountid=account_id,
                zip_code=zip_code,
                address=address,
                city=city,
                country=country,
                status=status
            )
            message = f"Account {account_id} created successfully"
            messages.success(request, message)
            return redirect('core:accounts')
        except Exception as e:
            message = f"Error: {e}"
            messages.error(request, message)
            return redirect('core:create_account')

    def generate_account_id1(self,prefix, model, id_field):
        # Ensure the prefix is not empty
        if not prefix:
            raise ValueError("Prefix cannot be empty")

        # Find the latest account ID in the database
        last_account = model.objects.order_by('-' + id_field).first()

        if last_account:
            last_id = getattr(last_account, id_field)
            if last_id.startswith(prefix):
                # Extract the numeric part of the last ID and increment it
                numeric_part = last_id[len(prefix):]
                new_numeric_part = str(int(numeric_part) + 1).zfill(len(numeric_part))
                new_account_id = prefix + new_numeric_part
            else:
                # If the last ID has a different prefix, start from 1
                new_account_id = prefix + '1'.zfill(len(last_id) - len(prefix))
        else:
            # If no accounts exist yet, start with '1'
            new_account_id = prefix + '1'

        return new_account_id

class AccountDetails(View):
    def get(self, request, account_id):
        account_details =  UserAccount.objects.get(accountid=account_id)
        transactions = Transactions.objects.filter(client_id = account_details.id)
        latest_balance = check_balance(transactions)

        context = {
            'title': 'Account Details',
            'account': account_details,
            'transactions': transactions,
            'account_balance': format(latest_balance,",")
        }
      
        return render(request, 'core/account-details.html', context)    
    
    def post(self, request, account_id):
        account_details = request.POST
        first_name = account_details.get('first_name')
        last_name = account_details.get('last_name')
        email = account_details.get('email')
        mobile = account_details.get('mobile')
        nationalid = account_details.get('nationalid')
        gender = account_details.get('gender')
        dob = account_details.get('dob')
        zip_code = account_details.get('zip_code')
        address = account_details.get('address')
        city = account_details.get('city')
        country = account_details.get('country')
        status = account_details.get('status')
        # print(first_name, last_name, email, mobile, nationalid, gender, dob, zip_code, address, city, country, status)
        try:
            UserAccount.objects.filter(accountid=account_id).update(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                nationalid=nationalid,
                gender=gender,
                dob=dob,
                zip_code=zip_code,
                address=address,
                city=city,
                country=country,
                status=status
            )
            message = f"Account {account_id} updated successfully"
            messages.success(request, message)
            return redirect('core:account_details', account_id)
        except Exception as e:
            message = f"Error: {e}"
            messages.error(request, message)        
            context = {
                'title': 'Account Details',
                'account': UserAccount.objects.get(accountid=account_id)
            }
            return render(request, 'core/account-details.html', context)

class DeleteAccount(View):
    def get(self, request, account_id):
        account = UserAccount.objects.get(accountid=account_id)
        account.delete()
        return redirect('core:accounts')   
    
class ActivateAccount(View):
    def get(self, request, account_id):
        account = UserAccount.objects.get(accountid=account_id)
        account.status = 'ACTIVE'
        account.save()
        message = f"Account {account_id} activated successfully"
        messages.success(request, message)
        return redirect('core:account_details', account_id)
    
class BlockAccount(View):
    def get(self, request, account_id):
        account = UserAccount.objects.get(accountid=account_id)
        account.status = 'BLOCKED'
        account.save()
        message = f"Account {account_id} blocked successfully"
        messages.success(request, message)
        return redirect('core:account_details', account_id)
    
class SuspendAccount(View):
    def get(self, request, account_id):
        account = UserAccount.objects.get(accountid=account_id)
        account.status = 'SUSPENDED'
        account.save()
        message = f"Account {account_id} suspended successfully"
        messages.success(request, message)
        return redirect('core:account_details', account_id)

class TransactionsListing(View):
    def get(self, request):
        context = {
            'title': 'Transactions Listing',
            'transactions': Transactions.objects.all()
        }
        return render(request, 'core/transactions.html', context)
    
class CreateDeposit(View):
    def get(self, request):
        context = {
            'title': 'Create Deposit'
        }
        return render(request, 'core/create-deposit.html', context)
    
    def post(self, request):
        account_id = request.POST.get('account_number')
        amount = request.POST.get('amount')
        date = datetime.date.today()
        new_balance = new_trx_balance(
                model=Transactions,
                client=UserAccount.objects.get(accountid=account_id),
                transaction_type='CREDIT',
                transaction_amount= int(amount),
            )  

        try:
            Transactions.objects.create(
                client = UserAccount.objects.get(accountid=account_id),
                transaction_type='CREDIT',
                transaction_date=date,
                transaction_amount=amount,
                transaction_balance=new_balance
            )
            message = f"Deposit of {amount} made successfully!"
            messages.success(request, message)
            return redirect('core:transactions')
        except Exception as e:
            message = f"Error: {e}"
            messages.error(request, message)
            return redirect('core:create_deposit')
        

class CreateWithdraw(View):
    def get(self, request):
        context = {
            'title': 'Withdraw Funds'
        }
        return render(request, 'core/create-withdrawal.html', context)
    
    def post(self, request):
        account_id = request.POST.get('account_number')
        amount = request.POST.get('amount')
        date = datetime.date.today()
        new_balance = new_trx_balance(
                model=Transactions,
                client=UserAccount.objects.get(accountid=account_id),
                transaction_type='DEBIT',
                transaction_amount= int(amount),
            )  

        try:
            # check existing balance
            transactions = Transactions.objects.filter(client_id = request.user.id)
            latest_balance = check_balance(transactions)
            if latest_balance < int(amount):
                message = f"Insufficient funds in account {account_id}!"
                messages.error(request, message)
                return redirect('core:account_details', account_id)
            Transactions.objects.create(
                client = UserAccount.objects.get(accountid=account_id),
                # client_id=account_id,
                transaction_type='DEBIT',
                transaction_date=date,
                transaction_amount=amount,
                transaction_balance=new_balance
            )
            message = f"Withdrawal of {amount} made successfully!"
            messages.success(request, message)
            return redirect('core:transactions')
        except Exception as e:
            message = f"Error: {e}"
            messages.error(request, message)
            return redirect('core:create_withdraw')
    



    
    




    