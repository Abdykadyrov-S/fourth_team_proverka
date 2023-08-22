from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from applications.services.constants import DISTRICT_CHOICES
from applications.users.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30, null=True, verbose_name='ФИО')
    login = models.CharField(max_length=30, unique=True, null=True, verbose_name='Введите логин')
    email = models.EmailField(null=True, unique=True, verbose_name='Введите свою почту')
    password = models.CharField(max_length=100, unique=True, verbose_name='Введите пароль')
    profile_photo = models.ImageField(blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    is_boss = models.BooleanField(default=False)
    district = models.CharField(
        max_length=100, choices=DISTRICT_CHOICES, blank=True, verbose_name='Район проверок сотрудника'
    )
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['password', 'email']

    objects = UserManager()

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        app_label = 'users'
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    time = models.DateTimeField()
