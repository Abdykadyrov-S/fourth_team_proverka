from rest_framework import serializers

from applications.boss.models import Task
from applications.verification.models import CheckList


class EmployeeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = '__all__'
