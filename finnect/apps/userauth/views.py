from typing import Any, Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from djoser.views import TokenCreateView
from djoser.views import User
from loguru import logger
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .utils import send_otp_email, generate_otp


User = get_user_model()


def set_auth_cookies(
    response: Response, access_token: str, refresh_token: Optional[str] = None
) -> None:
    access_token_lifetime = settings.SIMPLE_JWT[
        'ACCESS_TOKEN_LIFETIME'
    ].total_seconds()
    cookie_settings = {
        'path': settings.COOKIE_PATH,
        'secure': settings.COOKIE_SECURE,
        'httponly': settings.COOKIE_HTTPONLY,
        'samesite': settings.COOKIE_SAMESITE,
        'max_age': access_token_lifetime,
    }
    response.set_cookie('access', access_token, **cookie_settings)
    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT[
            'REFRESH_TOKEN_LIFETIME'
        ].total_seconds()
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings['max_age'] = refresh_token_lifetime
        response.set_cookie(
            'refresh', refresh_token, **refresh_cookie_settings
        )

    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings['httponly'] = False
    response.set_cookie('logged_in', 'true', **logged_in_cookie_settings)


class CustomTokenCreateView(TokenCreateView):
    def _action(self, serializer):
        user = serializer.user
        if user.is_account_blocked:
            return Response(
                {
                    'error': 'Account is blocked due to multiple failed login attempts.'
                    f'try again after {settings.BLOCKED_ACCOUNT_DURATION / 60} minutes.'
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user.reset_failed_login_attempts()

        otp = generate_otp()
        user.set_otp(otp)
        send_otp_email(user.email, otp)

        logger.info(f'OTP sent for login to user: {user.email}')

        return Response(
            {
                'message': 'OTP sent to your email address.',
                'email': user.email,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error(f'Error in login: {e}')
            email = request.data.get('email')
            user = User.objects.filter(email=email).first()
            if not user:
                return Response(
                    {'error': 'Invalid credentials.'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.handle_failed_login_attempts()
            failed_attempts = user.failed_login_attempts
            logger.error(
                f'Failed login attempts for user: {email} = {failed_attempts}'
            )
            if failed_attempts >= settings.MAX_LOGIN_ATTEMPTS:
                return Response(
                    {
                        'error': 'Account is blocked due to multiple failed login attempts.'
                        f'try again after {settings.BLOCKED_ACCOUNT_DURATION / 60} minutes.'
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        return self._action(serializer)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        refresh_token = request.COOKIES.get('refresh')
        if refresh_token:
            request.data['refresh'] = refresh_token

        refresh_response = super().post(request, *args, **kwargs)
        if not refresh_response.status_code == status.HTTP_200_OK:
            return refresh_response

        access_token = refresh_response.data.get('access')
        refresh_token = refresh_response.data.get('refresh')

        if not (access_token and refresh_token):
            error_message = (
                'Access or refresh token not found in refresh response data'
            )
            refresh_response.data['message'] = error_message
            logger.error(error_message)
            return refresh_response

        set_auth_cookies(refresh_response, access_token, refresh_token)
        refresh_response.data.pop('access', None)
        refresh_response.data.pop('refresh', None)
        refresh_response.data['message'] = 'Token refreshed successfully.'
        return refresh_response


class OTPVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request: Request) -> Response:
        otp = request.data.get('otp')

        if not otp:
            return Response(
                {'error': 'OTP is required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.filter(
            otp=otp, otp_expiration_time__gt=timezone.now()
        ).first()
        if not user:
            return Response(
                {'error': 'Invalid or expired OTP.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_account_blocked:
            return Response(
                {
                    'error': 'Account is blocked due to multiple failed login attempts.'
                    f'try again after {settings.BLOCKED_ACCOUNT_DURATION / 60} minutes.'
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user.verify_otp(otp)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        response = Response(
            {
                'success': 'OTP verified successfully.',
            },
            status=status.HTTP_200_OK,
        )
        set_auth_cookies(response, access_token, refresh_token)
        logger.info(
            f'User logged in successfully: {user.email} with OTP {otp}'
        )
        return response
