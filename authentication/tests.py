from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from user_management.models import Pengguna, Instruktur
import json

class RegisterViewTest(TestCase):
    """Test suite for RegisterView functionality"""
    
    def setUp(self):
        """Setup for tests - create APIClient"""
        self.client = APIClient()
        self.register_url = reverse('register')
        
        # Valid student data
        self.valid_student_data = {
            'username': 'teststudent',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'email': 'student@test.com',
            'first_name': 'Test',
            'last_name': 'Student',
            'role': 'student'
        }
        
        # Valid instructor data
        self.valid_instructor_data = {
            'username': 'testinstructor',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            'email': 'instructor@test.com',
            'first_name': 'Test',
            'last_name': 'Instructor',
            'role': 'instructor',
            'keahlian': 5
        }
    
    def test_student_registration_success(self):
        """Test successful student registration"""
        response = self.client.post(
            self.register_url,
            self.valid_student_data,
            format='json'
        )
        
        # Check status code and response structure
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Student registered successfully')
        
        # Check user was created correctly
        self.assertTrue(Pengguna.objects.filter(username='teststudent').exists())
        user = Pengguna.objects.get(username='teststudent')
        self.assertEqual(user.role, 'student')
        self.assertEqual(user.email, 'student@test.com')
        
        # Check tokens were generated
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
    
    def test_instructor_registration_success(self):
        """Test successful instructor registration"""
        response = self.client.post(
            self.register_url,
            self.valid_instructor_data,
            format='json'
        )
        
        # Check status code and response structure
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Instructor registered successfully')
        
        # Check user was created correctly
        self.assertTrue(Pengguna.objects.filter(username='testinstructor').exists())
        user = Pengguna.objects.get(username='testinstructor')
        self.assertEqual(user.role, 'instructor')
        
        # Check instructor profile was created
        self.assertTrue(hasattr(user, 'instruktur'))
        self.assertEqual(user.instruktur.keahlian, 5)
        
        # Check instructor-specific response data
        self.assertIn('instructor_id', response.data['user'])
        self.assertIn('keahlian', response.data['user'])
    
    def test_passwords_not_matching(self):
        """Test validation error when passwords don't match"""
        data = self.valid_student_data.copy()
        data['password2'] = 'DifferentPassword123!'
        
        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('password', response.data['errors'])
    
    def test_invalid_role(self):
        """Test validation error when role is invalid"""
        data = self.valid_student_data.copy()
        data['role'] = 'admin'  # Admin registration not allowed via API
        
        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('role', response.data['errors'])
    
    def test_missing_required_fields(self):
        """Test validation error when required fields are missing"""
        data = {
            'username': 'testuser',
            'password': 'TestPass123!',
            'password2': 'TestPass123!',
            # Missing email, first_name, last_name, role
        }
        
        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        
        # Check all required fields are in the error response
        error_fields = response.data['errors'].keys()
        self.assertIn('email', error_fields)
        self.assertIn('first_name', error_fields)
        self.assertIn('last_name', error_fields)
        self.assertIn('role', error_fields)
    
    def test_instructor_without_keahlian(self):
        """Test validation error when registering instructor without keahlian"""
        data = self.valid_instructor_data.copy()
        data.pop('keahlian')
        
        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')
        self.assertIn('keahlian', response.data['errors'])
