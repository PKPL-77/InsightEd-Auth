from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]
