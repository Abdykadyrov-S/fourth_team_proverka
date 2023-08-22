from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from applications.employee.serializes import EmployeeTaskSerializer
from applications.verification.permissions import IsEmployeePermission
from ..services.employee_services import get_employee_tasks, get_employee_checklists, update_task_read_status
from ..verification.serializer import CheckListSerializer


class EmployeeTaskListView(ListAPIView):
    serializer_class = EmployeeTaskSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]

    def get_queryset(self):
        user = self.request.user
        return get_employee_tasks(user)


class EmployeeCheckListView(ListAPIView):
    serializer_class = CheckListSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]

    def get_queryset(self):
        user = self.request.user
        return get_employee_checklists(user)


class TaskDetailView(RetrieveUpdateAPIView):
    serializer_class = EmployeeTaskSerializer
    permission_classes = [IsAuthenticated, IsEmployeePermission]

    def get_queryset(self):
        user = self.request.user
        return get_employee_tasks(user)

    def put(self, request, *args, **kwargs):
        task = self.get_object()

        if task.employee == self.request.user:
            task = update_task_read_status(task)
            serializer = self.get_serializer(task)
            return Response(serializer.data)