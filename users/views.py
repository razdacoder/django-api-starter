from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Create your views here.


class UserTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get(settings.AUTH_COOKIE)
            refresh_token = response.data.get(settings.AUTH_REFRESH_COOKIE)

            response.set_cookie(settings.AUTH_COOKIE, access_token,
                                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                                path=settings.AUTH_COOKIE_PATH,
                                secure=settings.AUTH_COOKIE_SECURE,
                                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                                samesite=settings.AUTH_COOKIE_SAME_SITE)
            response.set_cookie(settings.AUTH_REFRESH_COOKIE, refresh_token,
                                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                                path=settings.AUTH_COOKIE_PATH,
                                secure=settings.AUTH_COOKIE_SECURE,
                                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                                samesite=settings.AUTH_COOKIE_SAME_SITE)
        return response


class UserTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get(settings.AUTH_REFRESH_COOKIE)
        if refresh_token:
            request.data[settings.AUTH_REFRESH_COOKIE] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get(settings.AUTH_COOKIE)
            response.set_cookie(settings.AUTH_COOKIE, access_token,
                                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                                path=settings.AUTH_COOKIE_PATH,
                                secure=settings.AUTH_COOKIE_SECURE,
                                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                                samesite=settings.AUTH_COOKIE_SAME_SITE)
        return response


class UserTokenVerifyView(TokenVerifyView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        access_token = request.COOKIES.get(settings.AUTH_COOKIE)
        if access_token:
            request.data['token'] = access_token
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie(settings.AUTH_COOKIE)
        response.delete_cookie(settings.AUTH_REFRESH_COOKIE)
        return response


class UserSocialAuthView(ProviderAuthView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 201:
            access_token = response.data.get(settings.AUTH_COOKIE)
            refresh_token = response.data.get(settings.AUTH_REFRESH_COOKIE)

            response.set_cookie(settings.AUTH_COOKIE, access_token,
                                max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
                                path=settings.AUTH_COOKIE_PATH,
                                secure=settings.AUTH_COOKIE_SECURE,
                                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                                samesite=settings.AUTH_COOKIE_SAME_SITE)
            response.set_cookie(settings.AUTH_REFRESH_COOKIE, refresh_token,
                                max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
                                path=settings.AUTH_COOKIE_PATH,
                                secure=settings.AUTH_COOKIE_SECURE,
                                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                                samesite=settings.AUTH_COOKIE_SAME_SITE)
        return response
