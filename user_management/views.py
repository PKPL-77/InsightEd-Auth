from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .models import Pengguna, Admin, Instruktur
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        - Retrieve user profile details
        - Include user metadata
        - Handle privacy settings
        """
        # Get detailed user profile    
        user = get_object_or_404(Pengguna, id=request.user.id)
        
        # Basic user data available for all users
        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'user_id': str(user.user_id),
        }
        
        # Add role-specific data
        if user.role == 'admin':
            admin = Admin.objects.get(id=user.id)
            data['admin_id'] = str(admin.admin_id)
            data['is_staff'] = admin.is_staff
            data['is_superuser'] = admin.is_superuser
        
        elif user.role == 'instructor':
            instruktur = Instruktur.objects.get(id=user.id)
            data['instruktur_id'] = str(instruktur.instruktur_id)
            data['keahlian'] = instruktur.keahlian
        
        # Render template
        return render(request, 'user_management/profile.html', {'user': data})

    def post(self, request):
        """
        - Validate profile update data
        - Apply profile changes
        """
        user = get_object_or_404(Pengguna, id=request.user.id)
        
        try:
            data = request.POST
            
            # Update user fields
            if 'email' in data:
                user.email = data['email']
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'username' in data and user.username != data['username']:
                # Check if username is available
                if Pengguna.objects.filter(username=data['username']).exists():
                    messages.error(request, 'Username already taken')
                    return redirect('user_management:profile')
                user.username = data['username']
                
            # Role-specific updates
            if user.role == 'instructor' and 'keahlian' in data:
                instruktur = Instruktur.objects.get(id=user.id)
                instruktur.keahlian = data['keahlian']
                instruktur.save()
            
            user.save()
            
            messages.success(request, 'Profile updated successfully')
            return redirect('user_management:profile')
            
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
            return redirect('user_management:profile')

    def delete(self, request):
        """
        - Delete the user account
        - Return success/failure response
        """
        try:
            user = get_object_or_404(Pengguna, id=request.user.id)
            user.delete()
            
            messages.success(request, 'Your account has been deleted successfully')
            return redirect('authentication:login')
            
        except Exception as e:
            messages.error(request, f'Error deleting account: {str(e)}')
            return redirect('user_management:profile')

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Change user password
        """
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent logging out
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_management:profile')
        else:
            # Get user data for the template, similar to ProfileView
            user = get_object_or_404(Pengguna, id=request.user.id)
            user_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.role,
                'user_id': str(user.user_id),
            }
            
            # Add role-specific data
            if user.role == 'admin':
                admin = Admin.objects.get(id=user.id)
                user_data['admin_id'] = str(admin.admin_id)
                user_data['is_staff'] = admin.is_staff
                user_data['is_superuser'] = admin.is_superuser
            
            elif user.role == 'instructor':
                instruktur = Instruktur.objects.get(id=user.id)
                user_data['instruktur_id'] = str(instruktur.instruktur_id)
                user_data['keahlian'] = instruktur.keahlian
            
            messages.error(request, 'Password change failed. Please correct the errors below.')
            return render(request, 'user_management/profile.html', {
                'user': user_data,
                'password_form': form,
                'active_tab': 'security'  # This will help the template show the security tab
            })

class DeleteAccountView(APIView):
    """
    Handle account deletion and logging out the user
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Get the user from the request
            user = request.user
            
            # Log the user out first (important to do this before deleting)
            logout(request)
            
            # Delete the user account
            user.delete()
            
            messages.success(request, 'Your account has been deleted successfully')
            return redirect('home')
            
        except Exception as e:
            messages.error(request, f'Error deleting account: {str(e)}')
            return redirect('user_management:profile')
