from typing import Tuple, TypeVar

from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.tokens import Token

from .models import User

AuthUser = TypeVar("AuthUser", User, TokenUser)


class UserJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Tuple[User, Token] | None:

        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token
