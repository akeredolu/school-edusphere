from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.utils.translation import gettext_lazy as _

class CookieJWTAuthentication(JWTAuthentication):
    """
    Authenticate users via JWT stored in HttpOnly cookies.
    If the access token is expired, try to refresh it using the refresh token.
    """
    www_authenticate_realm = "api"

    def authenticate(self, request):
        # 1️⃣ Get tokens from cookies
        access_token = request.COOKIES.get("access_token")
        refresh_token = request.COOKIES.get("refresh_token")

        if not access_token:
            return None  # No access token → unauthenticated

        try:
            # 2️⃣ Validate access token
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
            return (user, validated_token)

        except TokenError:
            # Access token expired or invalid → try refresh
            if refresh_token:
                try:
                    refresh = RefreshToken(refresh_token)
                    new_access_token = str(refresh.access_token)

                    # Validate new access token
                    validated_token = self.get_validated_token(new_access_token)
                    user = self.get_user(validated_token)

                    # Attach new token to request for frontend/middleware to use if needed
                    request._new_access_token = new_access_token
                    return (user, validated_token)

                except TokenError:
                    # Refresh token invalid → require login
                    return None
            # No refresh token → require login
            return None

    def authenticate_header(self, request):
        return f'Bearer realm="{self.www_authenticate_realm}"'

