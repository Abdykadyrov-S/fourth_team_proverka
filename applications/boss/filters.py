import django_filters

from applications.users.models import User


class UserFilter(django_filters.FilterSet):
    district = django_filters.CharFilter(field_name='district')

    class Meta:
        model = User
        fields = ['district']
