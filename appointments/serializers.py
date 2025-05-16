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



class appointmentSerializer(serializers.ModelSerializer):

    """
    Serializer for the appointment model
    """
    class Meta:
        model = Appointment
        fields = [
            'user'
            'available_time'
            'is_confirmed'
        ]

        read_only_fields = [

        ]
