from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .serializers import UserSerializer
from .authentication import CookieJWTAuthentication

from django.views.decorators.csrf import csrf_exempt

# -----------------------
# CURRENT USER
# -----------------------
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CookieJWTAuthentication]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# -----------------------
# LOGIN
# -----------------------
@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if not user:
        return Response({"detail": "Invalid credentials"}, status=401)

    # Create tokens
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    response = Response({
        "detail": "Login successful",
        "role": user.role,
        "user": UserSerializer(user).data
    })

    # Set HttpOnly cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # True in production with HTTPS
        samesite="Lax",
        path="/",
        max_age=30*60,  # 30 minutes (match ACCESS_TOKEN_LIFETIME)
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        path="/",
        max_age=7*24*60*60,  # 7 days (match REFRESH_TOKEN_LIFETIME)
    )

    return response


# -----------------------
# LOGOUT
# -----------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    response = Response({"detail": "Logged out"}, status=200)
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return response


# -----------------------
# REFRESH ACCESS TOKEN
# -----------------------
@api_view(["POST"])
@permission_classes([AllowAny])
def refresh_token_view(request):
    refresh_token = request.COOKIES.get("refresh_token")
    if not refresh_token:
        return Response({"detail": "Refresh token missing"}, status=401)

    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)

        response = Response({"detail": "Token refreshed"})
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            path="/",
            max_age=30*60,  # 30 minutes
        )
        return response

    except TokenError:
        return Response({"detail": "Invalid refresh token"}, status=401)
