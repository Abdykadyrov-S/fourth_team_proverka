from django.urls import path
from .views import EstablishmentListCreateView, EstablishmentUpdateView

urlpatterns = [
    path('', EstablishmentListCreateView.as_view(), name='establishment-list'),
    path('<int:pk>/', EstablishmentUpdateView.as_view(), name='establishment-detail')
]
