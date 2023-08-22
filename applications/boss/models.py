from django.db import models

from applications.services.constants import ORGANIZATION_CHOICES
from applications.users.models import User


class Task(models.Model):
    type_organization = models.CharField(
        max_length=100, choices=ORGANIZATION_CHOICES, null=True, verbose_name='Тип организации'
    )
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_employee': True}  # Ограничиваем выборку только пользователями по проверяющим
    )
    is_read_by_employee = models.BooleanField(default=False)
    date_given = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_organization_display()} - {self.employee} - {self.is_read_by_employee}"

    class Meta:
        verbose_name = 'Задание сотрудника'
        verbose_name_plural = 'Задание сотрудника'