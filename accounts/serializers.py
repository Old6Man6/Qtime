from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import User
from accounts.models import phone_validator


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and partially updating the authenticated user's profile.
    """

    class Meta:
        model = User
        fields = ['phone',
                  'email',
                  'full_name',
                  'avatar',
                  'role']

        read_only_fields = ['phone', 'role']

    def validate_full_name(self, value: str) -> str:
        """
        Custom validation for full name field.
        """
        if len(value) < 3:
            raise serializers.ValidationError(_("Full name must be at least 3 characters long."))
        return value


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("phone",
                  "password",
                  "full_name")

    def create(self, validated_data):
        user = User.objects.create_user(
            phone=validated_data["phone"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name", "")
        )
        return user


"""================OTP section================="""


class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phone_validator])

    class Meta:
        fields = ['phone']


class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(validators=[phone_validator])
    code = serializers.CharField(min_length=4, max_length=4)

    class Meta:
        fields = ['phone', 'code']
