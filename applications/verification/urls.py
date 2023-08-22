from django.urls import path
from .views import CheckCreationView, CheckDetailView, \
    CheckItemListView, CheckItemDetailView, CheckListView, TrialCheckView

urlpatterns = [
    path('check_list/', CheckListView.as_view(), name='check-list'),
    path('checking/', CheckCreationView.as_view(), name='establishment-checking'),
    path('checking/<int:check_pk>/', CheckDetailView.as_view(), name='checking-detail'),
    path('checking/<int:check_pk>/check_items/', CheckItemListView.as_view(),
         name='check-items'),
    path('checking/<int:check_pk>/check_items/<int:item_pk>/',
         CheckItemDetailView.as_view(), name='check-item-update'),
    path('trial-check/', TrialCheckView.as_view(), name='trial-check'),
]
