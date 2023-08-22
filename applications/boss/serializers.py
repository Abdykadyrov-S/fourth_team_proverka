from rest_framework import serializers

from applications.boss.models import Task
from applications.users.models import User
from applications.verification.models import CheckList


class BossTaskSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_profile_photo = serializers.CharField(source='employee.profile_photo', read_only=True)
    employee_district = serializers.CharField(source='employee.district', read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        ref_name = 'UniqueNameForThisSerializer'  # Уникальное имя для этого сериализатора
        read_only_fields = ['is_read_by_employee', 'employee_name', 'employee_profile_photo', 'employee_district']


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = '__all__'


class BossPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'profile_photo', 'district']


class BossPageEmployeeSerializer(serializers.ModelSerializer):
    establishment_name = serializers.CharField(source='establishment.name', read_only=True)
    establishment_type = serializers.CharField(source='establishment.type', read_only=True)
    establishment_photo = serializers.CharField(source='establishment.photo', read_only=True)

    class Meta:
        model = CheckList
        fields = ['id', 'establishment_type', 'establishment_name', 'establishment_photo']
