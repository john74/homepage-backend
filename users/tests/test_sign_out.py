from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from users.views import SignOutAPIView, SignInAPIView

User = get_user_model()


class SignOutAPIViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user@app.com", password="user1234")
        self.factory = APIRequestFactory()
        self.sign_in_view = SignInAPIView.as_view()
        self.sign_out_view = SignOutAPIView.as_view()
        self.sign_in_url = reverse('users:sign_in')
        self.sign_in_out = reverse('users:sign_out')

    def test_sign_out_success(self):
        credentials = {"email":"user@app.com", "password":"user1234"}

        sign_in_request = self.factory.post(self.sign_in_url, credentials, format='json')
        sign_in_response = self.sign_in_view(sign_in_request)
        access_token = sign_in_response.data.get("access_token")

        sign_out_request = self.factory.post(self.sign_in_out, HTTP_AUTHORIZATION=f'JWT {access_token}')
        sign_out_response = self.sign_out_view(sign_out_request)

        self.assertEqual(sign_out_response.status_code, status.HTTP_200_OK)
        self.assertEqual(sign_out_response.data['message'], 'Successfully signed out')

    def test_sign_out_unauthorized_user(self):
        credentials = {"email":"user@invalid.com", "password":"user1234"}

        sign_in_request = self.factory.post(self.sign_in_url, credentials, format='json')
        sign_in_response = self.sign_in_view(sign_in_request)
        access_token = sign_in_response.data.get("access_token")

        sign_out_request = self.factory.post(self.sign_in_out, HTTP_AUTHORIZATION=f'JWT {access_token}')
        sign_out_response = self.sign_out_view(sign_out_request)

        self.assertEqual(sign_out_response.status_code, status.HTTP_401_UNAUTHORIZED)