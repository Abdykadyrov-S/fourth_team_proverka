from django.db import models

from applications.services.constants import ORGANIZATION_CHOICES
from ..users.models import User


class Establishment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=ORGANIZATION_CHOICES, null=True, verbose_name='Тип')
    name = models.CharField(max_length=100, null=True, verbose_name='Название')
    inn = models.PositiveIntegerField(verbose_name='ИНН', unique=True)
    start_time = models.TimeField(null=True, verbose_name='Начало работы')
    end_time = models.TimeField(null=True, verbose_name='Конец работы')
    address = models.TextField(max_length=200, verbose_name='Адрес')
    date_next_check = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='establishment_photos/', blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организация'
