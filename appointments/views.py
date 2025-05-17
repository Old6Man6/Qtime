from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Appointment, AvailableTime
from .serializers import AppointmentSerializer, AvailableTimeSerializer
from .filters import AvailableTimeFilter
from accounts.permissions import IsAdmin, IsProvider, IsRegularUser


# ✅ View for listing available slots with filters (branch, provider, service, time range)
class AvailableTimeListView(generics.ListAPIView):
    """
    List all available (not booked) time slots with filtering options.
    """
    queryset = AvailableTime.objects.filter(is_booked=False)
    serializer_class = AvailableTimeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AvailableTimeFilter


# ✅ Regular user can view and create their own appointments
class UserAppointmentView(generics.ListCreateAPIView):
    """
    Allow users to:
    - See their appointments
    - Create new appointments if the time is still available
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsRegularUser]

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        available_time = serializer.validated_data.get('available_time')
        if available_time.is_booked:
            raise PermissionDenied("This time slot is already booked.")
        available_time.mark_as_booked()
        serializer.save(user=self.request.user)


# ✅ Provider can view their appointments
class ProviderAppointmentListView(generics.ListAPIView):
    """
    Allow service providers to list appointments that belong to them.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def get_queryset(self):
        return Appointment.objects.filter(available_time__provider=self.request.user)


# ✅ Provider can delete only their own appointments
class ProviderAppointmentDeleteView(generics.DestroyAPIView):
    """
    Allow providers to delete only their own appointments and make the slot available again.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsProvider]

    def get_queryset(self):
        return Appointment.objects.filter(available_time__provider=self.request.user)

    def perform_destroy(self, instance):
        instance.available_time.mark_as_available()
        instance.delete()


# ✅ Admin can view all appointments in the system
class AdminAppointmentListView(generics.ListAPIView):
    """
    Admin view for listing all appointments.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]