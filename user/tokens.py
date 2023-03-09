from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
