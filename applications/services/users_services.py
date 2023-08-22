from django.contrib.auth import authenticate, hashers
from django.utils import timezone
from rest_framework import status, response
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from ..users import models
from ..users.emails import send_email_confirmation, send_email_reset_password
from ..users.models import User
from ..users.utils import code


class RegisterService:
    @staticmethod
    def create_user(serializer, request):
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_email_confirmation(user.email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyService:
    @staticmethod
    def verify_otp(serializer):
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        otp = serializer.data['otp']

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'Неверный email.'}, status=400)

        if user.otp != otp:
            return Response({'error': 'Неверный код подтверждения.'}, status=400)

        user.is_active = True
        user.save()

        return Response({'message': 'Аккаунт успешно подтвержден.'}, status=200)


class LoginService:
    @staticmethod
    def authenticate_user(login, password):
        user = authenticate(login=login, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)
            return Response({
                'message': 'Аутентификация прошла успешно',
                "status": status.HTTP_200_OK,
                "user": user.login,
                'email': user.email,
                "refresh_token": str(refresh),
                "access_token": str(access)
            })
        return Response(
            {'message': 'Неверный логин или пароль'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ResetPasswordSendEmail:

    @staticmethod
    def password_reset_email(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = serializer.validated_data["email"]
            user = models.User.objects.get(email=email)
        except:
            return response.Response(
                data={
                    "error": "Пользователь с указанным адресом электронной почты не найден."
                }
            )

        time = timezone.now() + timezone.timedelta(minutes=5)

        password_reset_token = models.PasswordResetToken(
            user=user, code=code, time=time
        )
        password_reset_token.save()

        send_email_reset_password(user.email)

        return response.Response(data={"detail": 'send'}, status=status.HTTP_200_OK)


class PasswordResetCode:
    @staticmethod
    def password_reset_code(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            code = serializer.validated_data["code"]
            reset_code = models.PasswordResetToken.objects.get(
                code=code, time__gt=timezone.now()
            )
        except Exception as e:
            return response.Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={
                    "error": f"Недействительный код для сброса пароля или время истечения кода закончилось.{e}"},
            )
        return response.Response(
            data={"detail": "success", "code": f"{code}"}, status=status.HTTP_200_OK)


class PasswordResetNewPassword:
    @staticmethod
    def password_reset_new_password(code, password):
        try:
            password_reset_token = models.PasswordResetToken.objects.get(
                code=code, time__gt=timezone.now()
            )
        except models.PasswordResetToken.DoesNotExist:
            return False, "Недействительный код для сброса пароля или время истечения кода закончилось."

        user = password_reset_token.user
        user.password = hashers.make_password(password)
        user.save()

        password_reset_token.delete()
        return True, "Пароль успешно сброшен."
