from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from applications.boss.filters import UserFilter
from applications.boss.models import Task
from applications.boss.serializers import BossPageSerializer, BossTaskSerializer, BossPageEmployeeSerializer
from applications.services.boss_services import BossPageService, BossPageEmployeeService, BossPageDetailUserService
from applications.verification.permissions import IsBossPermission


class BossPageView(ListAPIView):
    serializer_class = BossPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter

    permission_classes = [IsAuthenticated, IsBossPermission]

    def get_queryset(self):
        return BossPageService.get_annotated_employees_with_tasks()


class BossPageEmployeeView(ListAPIView):
    serializer_class = BossPageEmployeeSerializer
    permission_classes = [IsAuthenticated, IsBossPermission]

    def get_queryset(self):
        user_pk = self.kwargs.get('pk')
        return BossPageEmployeeService.get_checklists_for_employee(user_pk)


class BossPageDetailUserTasksView(ListAPIView):
    serializer_class = BossTaskSerializer
    permission_classes = [IsAuthenticated, IsBossPermission]

    def get_queryset(self):
        employee_pk = self.kwargs.get('pk')
        employee = BossPageDetailUserService.get_annotated_employee_with_tasks(employee_pk)
        if employee:
            return employee.tasks
        return []


class TaskCreateListView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = BossTaskSerializer
    permission_classes = [IsAuthenticated, IsBossPermission]
