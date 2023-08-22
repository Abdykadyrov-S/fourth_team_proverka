from django.urls import path
from applications.employee.views import EmployeeTaskListView, EmployeeCheckListView, TaskDetailView

urlpatterns = [
    path('tasks/', EmployeeTaskListView.as_view(), name='employee_task_list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('checks/', EmployeeCheckListView.as_view(), name='employee_check_list'),
]
