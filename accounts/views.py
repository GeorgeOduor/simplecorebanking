from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
# login view
class LoginView(View):
    def get(self, request):
        # check if user is authenticated
        if request.user.is_authenticated:
            # User is authenticated
            return redirect('core:home')
        else:
            # User is not authenticated
            contex = {
                'title': 'Login'
            }

            return render(request, 'accounts/login.html', contex)
    
    def post(self, request):
        login_data = request.POST
        username = login_data.get('username')
        password = login_data.get('password')
        user = authenticate(request, username=username, password=password)
        print(username, password, user,"--------------------------")
        if user:
            login(request, user)
            return redirect('core:home')
        else:
            return redirect('accounts:login')
        
    
class RegisterView(View):
    def get(self, request):
        contex = {
            'title': 'Register'
        }
        # check if user is authenticated
        if request.user.is_authenticated:
            # User is authenticated
            return redirect('core:home')
        else:
            return render(request, 'accounts/register.html', contex)
    
    def post(self, request):
        reg_data  = request.POST
        username  = reg_data.get('username')
        firstname = reg_data.get('firstname')
        lastname  = reg_data.get('lastname')
        email     = reg_data.get('email')
        password1 = reg_data.get('password1')
        password2 = reg_data.get('password2')
        try:
            if password1 != password2:
                message = f"Passwords do not match"
                messages.error(request, message)
                return redirect('accounts:register')
            
            user = User.objects.create_user(username, email, password1)
            user.first_name = firstname
            user.last_name  = lastname
            user.save()
            message = f"User {username} created successfully"
            messages.success(request, message)
            return redirect('accounts:login')
        except:
            message = f"User {username} already exists"
            messages.error(request, message)
            return redirect('accounts:register')
            
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('accounts:login')
        
class ForgotPasswordView(View):
    def get(self, request):
        contex = {
            'title': 'Forgot Password'
        }
        return render(request, 'accounts/forgot-password.html', contex)