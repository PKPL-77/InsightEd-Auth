from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .forms import LoginForm, RegisterForm

class LoginView(APIView):
    """
    Handle user login using Django session authentication
    """
    def get(self, request):
        # If user is already logged in, redirect to profile
        if request.user.is_authenticated:
            return redirect('/users/profile/')
        
        # Render login template with empty form
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})
    
    def post(self, request):
        form = LoginForm(request.POST)
        
        if form.is_valid():
            user = form.cleaned_data['user']
            
            # Create Django session
            login(request, user)
            
            # Set success message
            messages.success(request, f'Welcome back, {user.first_name}!')
            
            # Redirect to profile page
            return redirect('/users/profile/')
        
        # Authentication failed - form.errors will contain the error messages
        return render(request, 'authentication/login.html', {'form': form})

class LogoutView(APIView):
    """
    Handle user logout using Django session authentication
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Show logout confirmation page
        return render(request, 'authentication/logout_confirm.html')
    
    def post(self, request):
        # End Django session
        logout(request)
        
        # Set success message
        messages.success(request, 'You have been successfully logged out.')
        
        # Redirect to login page
        return redirect('/auth/login/')

class RegisterView(APIView):
    """
    Handle user registration for students and instructors only
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        # If user is already logged in, redirect to profile
        if request.user.is_authenticated:
            return redirect('/users/profile/')
        
        # Render registration template with empty form
        form = RegisterForm()
        return render(request, 'authentication/register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Create the user (form handles student vs instructor logic)
            user = form.save()
            
            # Automatically log in the new user
            login(request, user)
            
            # Set success message
            messages.success(request, f'Welcome to InsightED, {user.first_name}! Your account has been created.')
            
            # Redirect to profile page
            return redirect('/users/profile/')
        
        # Re-render the registration form with errors
        return render(request, 'authentication/register.html', {'form': form})
