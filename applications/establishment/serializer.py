from rest_framework import serializers
from applications.establishment.models import Establishment
from ..services.establishment_services import EstablishmentService


class EstablishmentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Establishment
        fields = '__all__'

    def get_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.id
        return None

    def validate_inn(self, value):
        return EstablishmentService.validate_inn(value)

    def create(self, validated_data):
        return EstablishmentService.create_establishment_instance(validated_data)

    def update(self, instance, validated_data):
        return EstablishmentService.update_establishment_instance(instance, validated_data)