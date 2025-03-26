import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class Pengguna(AbstractUser):
    """
    Base user model.
    Extends Django's AbstractUser for built-in authentication.
    """
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(max_length=50, default='student')
    
    # AbstractUser already provides:
    # - username
    # - password (properly hashed)
    # - first_name, last_name, email
    # - is_active, is_staff, etc.
    
    def __str__(self):
        return self.username

class Admin(Pengguna):
    """
    Admin user model for system administration.
    """
    admin_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    def save(self, *args, **kwargs):
        self.role = 'admin'
        self.is_staff = True
        self.is_superuser = True
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} - Admin"

class Instruktur(Pengguna):
    """
    Instructor model that inherits from Pengguna.
    """
    instruktur_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    keahlian = models.IntegerField()
    
    def save(self, *args, **kwargs):
        self.role = 'instructor'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.username} - Instructor"
