from rest_framework import serializers
from .models import Appointment, AvailableTime


class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Appointment
        fields = ['id', 'user', 'available_time', 'is_confirmed']
        read_only_fields = ['is_confirmed']

    def validate_available_time(self, value):
        """
        Validate that the selected available time is not already booked.
        """
        if value.is_booked:
            raise serializers.ValidationError("This time slot is already booked.")
        return value

    def create(self, validated_data):
        """
        Create an appointment and mark the available time as booked.
        """
        appointment = Appointment.objects.create(**validated_data)
        validated_data['available_time'].mark_as_booked()
        return appointment


class AvailableTimeSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(source='provider.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = AvailableTime
        fields = [
            'id', 'provider_name', 'service_name', 'branch_name',
            'start_time', 'duration_minutes', 'is_booked'
        ]
        read_only_fields = fields
