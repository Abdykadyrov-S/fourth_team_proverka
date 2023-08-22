from django.urls import path
from applications.boss.views import *

urlpatterns = [
    path('list_employee/', BossPageView.as_view(), name='list_employee'),
    path('employee/<int:pk>/', BossPageEmployeeView.as_view(), name='checks_employee'),
    path('employee/<int:pk>/tasks/', BossPageDetailUserTasksView.as_view(), name='employee_tasks'),
    path('tasks/', TaskCreateListView.as_view(), name='create_task'),
]
