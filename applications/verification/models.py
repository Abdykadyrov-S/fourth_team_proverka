from django.db import models
from rest_framework.exceptions import ValidationError

from applications.establishment.models import Establishment
from applications.services.constants import CHECK_LIST_CHOICES, CHOICE_IS_APPROVED
from applications.users.models import User


class ListPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Пункт')
    article_information = models.CharField(max_length=150, default='SET_NULL', verbose_name='Информация о статье')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Пункт"
        verbose_name_plural = "Пункты"


class CheckList(models.Model):
    establishment = models.ForeignKey(Establishment, on_delete=models.CASCADE)
    date_started = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    type_of_verification = models.CharField(
        max_length=20,
        choices=CHECK_LIST_CHOICES,
        default='PLANNED',
    )
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    representative_name = models.CharField(max_length=255, verbose_name='ФИО представителя организации', null=True)

    def __str__(self):
        return f"Check for {self.establishment.name} on {self.date_started}"


class CommonListPost(models.Model):
    post = models.TextField(max_length=100, blank=True, verbose_name='Дополнительная информация')
    is_approved = models.CharField(
        choices=CHOICE_IS_APPROVED, max_length=100, null=True, blank=True, verbose_name='Соответствие'
    )
    image = models.ImageField(null=True, blank=True, verbose_name='Фото')
    check_points = models.ForeignKey(ListPost, on_delete=models.CASCADE, related_name='пункты')
    check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.check_points.title}"

    class Meta:
        verbose_name = "Заполненные общие списки"
        verbose_name_plural = "Заполненные общие списки сотрудника"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TrialCheck(models.Model):
    check_point = models.ForeignKey(ListPost, on_delete=models.CASCADE, related_name='trial_checks')
    is_approved = models.BooleanField(default=False)