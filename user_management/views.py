from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
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
            
        return JsonResponse(data)

    def post(self, request):
        """
        - Validate profile update data
        - Apply profile changes
        """
        user = get_object_or_404(Pengguna, id=request.user.id)
        
        try:
            # For JSON data
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
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
                    return JsonResponse({
                        'success': False, 
                        'message': 'Username already taken'
                    }, status=400)
                user.username = data['username']
                
            # Role-specific updates
            if user.role == 'instructor' and 'keahlian' in data:
                instruktur = Instruktur.objects.get(id=user.id)
                instruktur.keahlian = data['keahlian']
                instruktur.save()
            
            user.save()
            
            return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    def delete(self, request):
        """
        - Delete the user account
        - Return success/failure response
        """
        try:
            user = get_object_or_404(Pengguna, id=request.user.id)
            user.delete()
            return JsonResponse({'success': True, 'message': 'User account deleted successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
