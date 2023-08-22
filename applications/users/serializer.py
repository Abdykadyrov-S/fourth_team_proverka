from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from applications.users.models import User


class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=6)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    login = serializers.CharField(min_length=6, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=30)
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["token"]


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'profile_photo', 'email']


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PasswordResetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        style={"input_type": "password"}, help_text="min lenght 4", min_length=4
    )


class PasswordResetCodeSerializer(serializers.Serializer):
    code = serializers.CharField()


class PasswordResetSearchUserSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']
