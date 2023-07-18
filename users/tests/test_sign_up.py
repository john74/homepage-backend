from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from users.views import SignUpAPIView

User = get_user_model()


class SignUpAPIViewTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SignUpAPIView.as_view()
        self.url = reverse('users:sign_up')

    def test_signup_success(self):
        signup_data = {
            "email": "user@app.com",
            "password": "user1234"
        }
        request = self.factory.post(self.url, data=signup_data)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User created successfully')

    def test_signup_password_less_than_eight_characters(self):
        signup_data = {
            "email": "user@app.com",
            "password": "user1"
        }
        request = self.factory.post(self.url, data=signup_data)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message']['password'][0], 'Ensure this field has at least 8 characters.')

    def test_signup_password_user_already_exists(self):
        user = User.objects.create_user(email="user@app.com", password="user1234")
        signup_data = {
            "email": "user@app.com",
            "password": "user1234"
        }
        request = self.factory.post(self.url, data=signup_data)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message']['email'][0], 'user with this email already exists.')