from rest_framework import serializers
from .models import Branch, Service


class BranchSerializer(serializers.ModelSerializer):
    """
    Branch serializers
    """
    class Meta:
        model = Branch
        fields = [
            'id',
            'name',
            'location',
            'phone_number'
        ]
        read_only_fields = [
            'id',
            'name',
            'location',
            'phone_number'
        ]


class ServiceSerializer(serializers.ModelSerializer):
    """
    Service serializers
    """
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'description',
            'price',
            'duration_minutes'
        ]
        read_only_fields = [
            'id',
            'name',
            'description',
            'price',
            'duration_minutes'
        ]