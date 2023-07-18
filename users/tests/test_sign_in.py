from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from users.views import SignInAPIView

User = get_user_model()


class SignInAPIViewTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = SignInAPIView.as_view()
        self.url = reverse('users:sign_in')
        self.user = User.objects.create_user(email="user@app.com", password="user_1234")

    def test_signin_success(self):
        request = self.factory.post(self.url, data={"email":"user@app.com", "password":"user_1234"})
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refreshToken', response.cookies)

    def test_signin_invalid_credentials(self):
        request = self.factory.post(self.url, data={"email":"invalid_user@app.com", "password":"user_1234"})
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid credentials')
        self.assertNotIn('access_token', response.data)
        self.assertNotIn('refreshToken', response.cookies)

    def test_signin_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        request = self.factory.post(self.url)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Invalid credentials')
        self.assertNotIn('access_token', response.data)
        self.assertNotIn('refreshToken', response.cookies)