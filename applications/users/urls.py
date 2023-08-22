from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserProfileView, VerifyOTP, RegisterViewSet, LoginViewSet, PasswordResetRequestAPIView, \
    PasswordResetNewPasswordAPIView, PasswordResetCodeAPIView, LogoutView

urlpatterns = [
    path('login/', LoginViewSet.as_view(), name="login"),
    path('register/', RegisterViewSet.as_view(), name='signup'),
    path('verify/', VerifyOTP.as_view(), name='confirm'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path("reset-password-email/", PasswordResetRequestAPIView.as_view(), name="search user and send mail"),
    path("reset-password-code/", PasswordResetCodeAPIView.as_view(), name="write code"),
    path("reset-new-password/<str:code>/", PasswordResetNewPasswordAPIView.as_view(), name="write new password"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
