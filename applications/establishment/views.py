from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from applications.establishment.models import Establishment
from applications.establishment.serializer import EstablishmentSerializer
from ..services.establishment_services import EstablishmentService


class EstablishmentListCreateView(ListCreateAPIView):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return EstablishmentService.create_establishment(serializer, request)


class EstablishmentUpdateView(RetrieveUpdateAPIView):
    queryset = Establishment.objects.all()
    serializer_class = EstablishmentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        establishment = self.get_object()
        return EstablishmentService.update_establishment(serializer, establishment, self.request)
