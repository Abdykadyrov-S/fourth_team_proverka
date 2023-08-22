from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from applications.establishment.models import Establishment


class EstablishmentService:
    @staticmethod
    def create_establishment(serializer, request):
        establishment = serializer.save(user=request.user)

        photo = request.FILES.get('photo')
        if photo:
            establishment.photo = photo
            establishment.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def update_establishment(serializer, establishment, request):
        if establishment.user != request.user:
            return Response(
                {'error': 'Вы не можете редактировать эту организацию.'},
                status=status.HTTP_403_FORBIDDEN
            )

        new_photo = request.data.get('photo')
        if new_photo:
            establishment.photo = new_photo
            establishment.save()

        serializer.save()
        return Response(serializer.data)

    @staticmethod
    def validate_inn(inn):
        if len(str(inn)) != 11:
            raise ValidationError("ИНН должен состоять из 11 цифр.")
        return inn

    @staticmethod
    def create_establishment_instance(validated_data):
        return Establishment.objects.create(**validated_data)

    @staticmethod
    def update_establishment_instance(instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
