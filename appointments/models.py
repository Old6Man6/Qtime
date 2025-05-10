from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from typing import Optional


class AvailableTime(models.Model):
    """
    Model to represent available time slots for service providers.
    """
    provider: 'models.ForeignKey' = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        verbose_name=_("Provider")
    )

    service: 'models.ForeignKey' = models.ForeignKey(
        'branches.Service',
        on_delete=models.CASCADE,
        verbose_name=_("Service")
    )

    branch: 'models.ForeignKey' = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        verbose_name=_("Branch")
    )

    start_time: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Start time")
    )

    duration_minutes: int = models.PositiveIntegerField(
        verbose_name=_("Duration (minutes)")
    )

    is_booked: bool = models.BooleanField(
        default=False,
        verbose_name=_("Is booked")
    )

    def __str__(self) -> str:
        return f"Provider {self.provider} - {self.service.name} at {self.start_time}"

    @property
    def end_time(self) -> str:
        """
        Calculate the end time based on start time and duration.
        """
        return self.start_time + timedelta(minutes=self.duration_minutes)

    def mark_as_booked(self) -> None:
        """
        Mark the time slot as booked.
        """
        self.is_booked = True
        self.save()

    def mark_as_available(self) -> None:
        """
        Mark the time slot as available again.
        """
        self.is_booked = False
        self.save()

    @classmethod
    def reserve_time_slot(
        cls,
        provider: 'accounts.User',
        service: 'branches.Service',
        start_time,
        duration_minutes: int
    ) -> bool:
        """
        Reserve a time slot if it's available.
        """
        end_time = start_time + timedelta(minutes=duration_minutes)

        available_slot = cls.objects.filter(
            provider=provider,
            start_time=start_time,
            duration_minutes=duration_minutes
        ).first()

        if available_slot and not available_slot.is_booked:
            available_slot.mark_as_booked()
            cls.objects.filter(
                provider=provider,
                start_time__gte=start_time,
                start_time__lt=end_time
            ).update(is_booked=True)
            return True
        return False


class Appointment(models.Model):
    """
    Model to represent an appointment made by a user.
    """
    user: 'models.ForeignKey' = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )

    service: 'models.ForeignKey' = models.ForeignKey(
        'branches.Service',
        on_delete=models.CASCADE,
        verbose_name=_("Service")
    )

    branch: 'models.ForeignKey' = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        verbose_name=_("Branch")
    )

    provider: 'models.ForeignKey' = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='provider_appointments',
        verbose_name=_("Provider")
    )

    appointment_time: models.DateTimeField = models.DateTimeField(
        verbose_name=_("Appointment time")
    )

    is_confirmed: bool = models.BooleanField(
        default=False,
        verbose_name=_("Is confirmed")
    )

    def __str__(self) -> str:
        return f"Appointment for {self.user} at {self.branch.name} with {self.provider.full_name} on {self.appointment_time}"

    def confirm_appointment(self) -> None:
        self.is_confirmed = True
        self.save()

    def cancel_appointment(self) -> None:
        self.is_confirmed = False
        self.save()
