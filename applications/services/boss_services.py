from django.db.models import Prefetch

from applications.boss.models import Task
from applications.users.models import User
from applications.verification.models import CheckList


class BossPageService:
    @staticmethod
    def get_annotated_employees_with_tasks():
        return User.objects.filter(is_employee=True).prefetch_related(
            Prefetch('task_set', queryset=Task.objects.all(), to_attr='tasks')
        )


class BossPageEmployeeService:
    @staticmethod
    def get_checklists_for_employee(user_pk):
        return CheckList.objects.filter(user=user_pk)


class BossPageDetailUserService:
    @staticmethod
    def get_annotated_employee_with_tasks(employee_pk):
        employee = User.objects.filter(is_employee=True, pk=employee_pk).prefetch_related(
            Prefetch('task_set', queryset=Task.objects.all(), to_attr='tasks')
        ).first()
        return employee
