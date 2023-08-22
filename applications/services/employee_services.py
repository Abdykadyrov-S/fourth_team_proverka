from django.http import Http404
from applications.boss.models import Task
from applications.verification.models import CheckList


def get_employee_tasks(user):
    return Task.objects.filter(employee=user)


def get_employee_checklists(user):
    queryset = CheckList.objects.filter(user=user)
    if not queryset.exists():
        raise Http404("У вас нет доступных проверок.")
    return queryset


def update_task_read_status(task):
    task.is_read_by_employee = True
    task.save()
    return task