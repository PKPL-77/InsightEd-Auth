from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from user_management.models import Pengguna, Instruktur


class LoginForm(forms.Form):
    """
    Form for user login
    """
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput)
    
    def clean(self):
        """
        Validate the username and password and set the authenticated user
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username', '')
        password = cleaned_data.get('password', '')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise ValidationError("User account is disabled.")
                cleaned_data['user'] = user
                return cleaned_data
            raise ValidationError("Unable to log in with provided credentials.")
        raise ValidationError("Must include 'username' and 'password'.")


class RegisterForm(forms.ModelForm):
    """
    Form for user registration with role-specific fields
    """
    password = forms.CharField(
        widget=forms.PasswordInput, 
        required=True, 
        validators=[validate_password]
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput, 
        required=True,
        label="Confirm Password"
    )
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    keahlian = forms.IntegerField(required=False, min_value=1, max_value=10, 
                                 label="Expertise Level (1-10)")
    
    class Meta:
        model = Pengguna
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'role', 'keahlian')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make these fields required
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
    
    def clean_role(self):
        """
        Validates that the role is allowed
        """
        role = self.cleaned_data.get('role')
        allowed_roles = ['student', 'instructor']
        if role not in allowed_roles:
            raise ValidationError(
                f"Role must be one of {allowed_roles}. Admin registration is not allowed."
            )
        return role
    
    def clean(self):
        """
        Validates the form data as a whole
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        role = cleaned_data.get('role')
        keahlian = cleaned_data.get('keahlian')
        
        if password and password2 and password != password2:
            self.add_error('password2', "Password fields didn't match.")
        
        # If role is instructor, keahlian is required
        if role == 'instructor' and not keahlian:
            self.add_error('keahlian', "This field is required for instructors.")
            
        return cleaned_data
    
    def save(self, commit=True):
        """
        Custom save method to handle different user types
        """
        # Don't call save yet to prevent database query
        instance = super().save(commit=False)
        
        # Get the role from cleaned data
        role = self.cleaned_data.get('role')
        
        # Set the password directly
        instance.set_password(self.cleaned_data.get('password'))
        
        if role == 'instructor':
            # Create an instructor with keahlian
            if commit:
                # We don't save the instance from ModelForm - instead, we create a specific type
                instructor = Instruktur(
                    keahlian=self.cleaned_data.get('keahlian'),
                    username=instance.username,
                    email=instance.email,
                    first_name=instance.first_name,
                    last_name=instance.last_name
                )
                instructor.set_password(self.cleaned_data.get('password'))
                instructor.save()
                return instructor
            return instance
        else:
            # Regular student creation
            if commit:
                instance.save()
            return instance