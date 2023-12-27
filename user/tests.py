from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse


class ProfileViewTestCase(TestCase):

    def setUp(self):
        # Set up a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        # Define the URL for the profile view
        self.url = reverse('profile')

    def test_get_profile_view(self):
        # Test GET request to the profile view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(response, 'registrations/profile.html')  # Check the correct template is used

    def test_post_profile_view(self):
        # Test POST request to the profile view
        data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'phone_number': '1234567890',
            'address_1': 'Street 1',
            'city': 'Sofia',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Check for a redirect after a successful post
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'newemail@example.com')  # Check the user's email is updated
        self.assertEqual(self.user.userprofile.phone_number, '1234567890')  # Check the user's profile is updated


class RegisterViewTestCase(TestCase):
    def setUp(self):
        # Define the URL for the register view
        self.url = reverse('register')

    def test_get_register_view(self):
        # Test GET request to the register view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(response, 'registrations/register.html')  # Check the correct template is used

    def test_post_register_view(self):
        # Test POST request to the register view
        data = {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Check for a redirect after a successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Check the new user exists


class LoginViewTestCase(TestCase):
    def setUp(self):
        # Set up a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Define the URL for the login view
        self.url = reverse('login')

    def test_get_login_view(self):
        # Test GET request to the login view
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Check for a successful response
        self.assertTemplateUsed(response, 'registrations/login.html')  # Check the correct template is used

    def test_post_login_view(self):
        # Test POST request to the login view
        data = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)  # Check for a redirect after a successful login
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)  # Check for a single message in the response
        self.assertEqual(str(messages[0]), f'You are logged in as {data["username"]}')  # Check the login message
