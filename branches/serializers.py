from rest_framework import serializers
from .models import Branch, Service
from django.utils.translation import gettext_lazy as _


class BranchSerializer(serializers.ModelSerializer):
    """
    Serializer for reading and writing Branch data.
    Only admin users should be allowed to create or update via views.
    """

    class Meta:
        model = Branch
        fields = ['id',
                  'name',
                  'location',
                  'phone_number']

        read_only_fields = ['id']  # id is auto-generated


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for services offered in branches.
    """

    class Meta:
        model = Service
        fields = ['id',
                  'name',
                  'description',
                  'duration_minutes',
                  'price']

        read_only_fields = ['id']