from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (
    LoginSerializer, TokenSerializer, 
    RefreshTokenSerializer, RegisterSerializer, LogoutSerializer
)
from .utils.token_generator import generate_jwt_token

class LoginView(APIView):
    """
    Handle user login and token generation
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
    Handle user logout and token blacklisting
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_205_RESET_CONTENT)

class TokenRefreshView(APIView):
    """
    Refresh access token using refresh token
    """
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                refresh = RefreshToken(serializer.validated_data['refresh'])
                data = {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
                
                return Response({
                    'status': 'success',
                    'tokens': data
                }, status=status.HTTP_200_OK)
            except TokenError:
                return Response({
                    'status': 'error',
                    'message': 'Invalid or expired token'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    """
    Handle user registration for students and instructors only
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Create the user (serializer handles student vs instructor logic)
            user = serializer.save()
            
            # Generate tokens for the new user
            refresh = RefreshToken.for_user(user)
            data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            
            token_serializer = TokenSerializer(data=data)
            token_serializer.is_valid()
            
            response_data = {
                'status': 'success',
                'message': f"{user.role.capitalize()} registered successfully",
                'user': {
                    'id': str(user.user_id),
                    'username': user.username,
                    'email': user.email,
                    'role': user.role
                },
                'tokens': token_serializer.data
            }
            
            # Add instructor-specific data if applicable
            if user.role == 'instructor':
                response_data['user']['instructor_id'] = str(user.instruktur_id)
                response_data['user']['keahlian'] = user.keahlian
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
