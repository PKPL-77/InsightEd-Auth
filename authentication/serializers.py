from rest_framework import serializers
from django.contrib.auth import authenticate
from user_management.models import Pengguna, Instruktur
from django.contrib.auth.password_validation import validate_password

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    
    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                data['user'] = user
                return data
            raise serializers.ValidationError("Unable to log in with provided credentials.")
        raise serializers.ValidationError("Must include 'username' and 'password'.")

class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    keahlian = serializers.IntegerField(required=False, write_only=True)
    
    class Meta:
        model = Pengguna
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role', 'keahlian')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'role': {'required': True}
        }
    
    def validate_role(self, value):
        """
        Check that the role is either 'student' or 'instructor'.
        """
        allowed_roles = ['student', 'instructor']
        if value not in allowed_roles:
            raise serializers.ValidationError(
                f"Role must be one of {allowed_roles}. Admin registration is not allowed through API."
            )
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # If role is instructor, keahlian is required
        if attrs.get('role') == 'instructor' and 'keahlian' not in attrs:
            raise serializers.ValidationError({"keahlian": "This field is required for instructors."})
            
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        role = validated_data.get('role')
        
        # Handle instructor creation
        if role == 'instructor':
            keahlian = validated_data.pop('keahlian')
            user = Pengguna.objects.create_user(**validated_data)
            Instruktur.objects.create(
                pengguna_ptr_id=user.id,
                keahlian=keahlian
            )
            return user
        
        # Regular student creation
        else:
            if 'keahlian' in validated_data:
                validated_data.pop('keahlian')  # Remove if accidentally included
            return Pengguna.objects.create_user(**validated_data)
