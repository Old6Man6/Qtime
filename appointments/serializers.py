from rest_framework import serializers
from .models import AvailableTime, Appointment

class AvailableTimeSerializer(serializers.ModelSerializer):
    """
    Serializer for the AvailableTime model
    """
    class Meta:
        model = AvailableTime
        fields = [
            'id',
            'provider',
            'service',
            'branch',
            'start_time',
            'duration_minutes',
            'is_booked',
        ]
        read_only_fields = [
            'id',
            'duration_minutes',
            'is_booked',
        ]
