"""Social login view"""
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings


class GoogleLogin(SocialLoginView):
    """Google login view"""
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_AUTH_CALLBACK_URL
    client_class = OAuth2Client
