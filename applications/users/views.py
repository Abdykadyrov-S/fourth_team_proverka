from rest_framework import status, generics, response
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from applications.users.models import User
from applications.users.serializer import RegisterSerializer, VerifySerializer, UserProfileSerializer, \
    PasswordChangeSerializer, LoginSerializer
from ..services.users_services import RegisterService, VerifyService, LoginService, ResetPasswordSendEmail, \
    PasswordResetCode, PasswordResetNewPassword
from applications.users import serializer


class RegisterViewSet(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        return RegisterService.create_user(self.serializer_class(data=request.data), request)


class VerifyOTP(APIView):
    serializer_class = VerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        return VerifyService.verify_otp(serializer)


class LoginViewSet(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')
        return LoginService.authenticate_user(login, password)


class UserProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.request.user.id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        name = request.data.get('name')
        profile_photo = request.data.get('profile_photo')

        if name:
            user.name = name
        if profile_photo:
            user.profile_photo = profile_photo

        user.save()

        if 'old_password' in request.data and 'new_password' in request.data:
            change_password_response = self.change_password(request)
            if change_password_response.status_code != 200:
                return change_password_response

        return Response(serializer.data)

    def change_password(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=self.request.user.id)
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data.get('old_password')
        new_password = serializer.validated_data.get('new_password')

        if not user.check_password(old_password):
            return Response(
                {'error': 'Старый пароль указан неверно.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if old_password == new_password:
            return Response(
                {'error': 'Новый пароль не должен совпадать со старым паролем.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Пароль успешно изменен.'}, status=status.HTTP_201_CREATED)


class PasswordResetRequestAPIView(generics.CreateAPIView):
    # для отправки кода на почту

    serializer_class = serializer.PasswordResetSearchUserSerializer

    def post(self, request, *args, **kwargs):
        reset_password_service = ResetPasswordSendEmail()
        return reset_password_service.password_reset_email(self, request)


class PasswordResetCodeAPIView(generics.CreateAPIView):
    # подтверждение кода

    serializer_class = serializer.PasswordResetCodeSerializer

    def post(self, request, *args, **kwargs):
        reset_password_code = PasswordResetCode()
        return reset_password_code.password_reset_code(self, request)


class PasswordResetNewPasswordAPIView(generics.CreateAPIView):
    # сброс пароля

    serializer_class = serializer.PasswordResetNewPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = kwargs["code"]
            password = serializer.validated_data["password"]
            success, message = PasswordResetNewPassword.password_reset_new_password(code, password)
            if success:
                return response.Response(data={"detail": message}, status=status.HTTP_200_OK)
            else:
                return response.Response(data={"detail": message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = RefreshToken(request.data.get('refresh_token'))
            refresh_token.blacklist()
            return Response({"message": "Вы успешно вышли из аккаунта"})
        except Exception as e:
            return Response({"error": "Произошла ошибка при выходе из аккаунта"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)