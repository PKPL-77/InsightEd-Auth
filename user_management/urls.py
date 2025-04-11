from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('password/change/', views.ChangePasswordView.as_view(), name='change_password'),
    path('account/delete/', views.DeleteAccountView.as_view(), name='delete_account'),
]
