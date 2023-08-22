from rest_framework import serializers

from applications.verification.models import CommonListPost, CheckList, TrialCheck, ListPost


class CommonListPostSerializer(serializers.ModelSerializer):
    check_points_title = serializers.CharField(source='check_points.title', read_only=True)
    article_information = serializers.CharField(source='check_points.article_information', read_only=True)

    class Meta:
        model = CommonListPost
        exclude = ['check_list', 'check_points']
        read_only_fields = ['check_points_title', 'article_information']


class CheckSerializer(serializers.ModelSerializer):
    establishment_id = serializers.CharField(source='establishment.id')

    class Meta:
        model = CheckList
        fields = ['establishment_id', 'representative_name']


class CheckListSerializer(serializers.ModelSerializer):
    establishment_photo = serializers.CharField(source='establishment.photo', read_only=True)
    establishment_type = serializers.CharField(source='establishment.type', read_only=True)
    establishment_name = serializers.CharField(source='establishment.name', read_only=True)
    establishment_id = serializers.CharField(source='establishment.id', read_only=True)

    class Meta:
        model = CheckList
        fields = ['id', 'establishment_photo', 'establishment_type', 'establishment_name', 'establishment_id']
        ref_name = 'UniqueNameForThisSerializer'  # Уникальное имя для этого сериализатора


class CheckDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = '__all__'
        read_only_fields = ['user', 'establishment']


class TrialCheckSerializer(serializers.ModelSerializer):
    # check_point = serializers.PrimaryKeyRelatedField(queryset=ListPost.objects.all())
    check_points_title = serializers.CharField(source='check_point.title', read_only=True)
    article_information = serializers.CharField(source='check_point.article_information', read_only=True)

    class Meta:
        model = TrialCheck
        fields = ['check_points_title', 'article_information', 'is_approved']
