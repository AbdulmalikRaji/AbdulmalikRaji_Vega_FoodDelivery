from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserTests(APITestCase):

    def setUp(self):
        """Create test users"""
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="TestPass123", is_verified=True)
        self.unverified_user = User.objects.create_user(username="unverified", email="unverified@example.com", password="TestPass123", is_verified=False)

    def test_signup_success(self):
        """Test user signup API"""
        url = reverse('signup')
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "NewPass123",
            "confirm_password":"NewPass123",
            "first_name": "firstname",
            "last_name": "lastname",
            "delivery_location": "123 Main St, City, State, Zip",
            "latitude": 6.7749,
            "longitude": 8.4194
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_success(self):
        """Test login API with correct credentials"""
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "TestPass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        url = reverse('login')
        data = {
            "username": "testuser",
            "password": "WrongPass"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_email_verification(self):
        """Test email verification endpoint"""
        uid = self.unverified_user.pk
        token = "testtoken"  # Mocked token
        url = reverse('email-verified', kwargs={"uidb64": uid, "token": token})
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])

    def test_password_reset_request(self):
        """Test forgot password request"""
        url = reverse('forgot-password')
        data = {"email": "test@example.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        """Test JWT token refresh"""
        refresh = RefreshToken.for_user(self.user)
        url = reverse('token-refresh')
        response = self.client.post(url, {"refresh": str(refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
