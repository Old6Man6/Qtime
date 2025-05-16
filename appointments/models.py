from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from typing import Optional


class AvailableTime(models.Model):
    """
    Model to represent available time slots for service providers.
    provider, service, branch, start_time, duration_minutes, is_booked
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
        editable=False,
        verbose_name=_("Duration (minutes)")
    )

    is_booked: bool = models.BooleanField(
        default=False,
        verbose_name=_("Is booked")
    )

    class Meta:
        verbose_name = _("Available Time")
        verbose_name_plural = _("Available Times")
        ordering = ['start_time']
        constraints = [
            models.UniqueConstraint(
                fields=["provider", "start_time"],
                name="unique_provider_time_slot"
            )
        ]


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
        branch: 'branches.Branch',
        start_time,
        duration_minutes: int
    ) -> bool | list:
        """
        Reserve a time slot if it's available.
        """
        end_time = start_time + timedelta(minutes=duration_minutes)

        conflict_exists = cls.objects.filter(
            provider=provider,
            branch=branch,
            service=service,
            is_booked=True,
            start_time__lt=end_time,
        ).annotate(
            real_end_time=models.ExpressionWrapper(
                models.F('start_time') + models.ExpressionWrapper(
                    models.F('duration_minutes') * 60,
                    output_field=models.DurationField()
                ),
                output_field=models.DateTimeField()
            )
        ).filter(real_end_time__gt=start_time).exists()

        if conflict_exists:
            raise ValueError("This time overlaps with an already booked slot.")


        available_slot = cls.objects.filter(
            provider=provider,
            start_time=start_time,
            branch=branch,
            duration_minutes=duration_minutes,
            is_booked=False
        ).first()

        if available_slot and not available_slot.is_booked:
            available_slot.mark_as_booked()
            cls.objects.filter(
                provider=provider,
                service=service,
                branch=branch,
                start_time__gte=start_time,
                start_time__lt=end_time
            ).update(is_booked=True)

            return True

        elif not available_slot or available_slot.is_booked:
            alternative_slots = cls.objects.filter(
                provider=provider,
                service=service,
                branch=branch,
                is_booked=False,
                start_time__gt=start_time
            ).order_by('start_time')  # limit to next 5 available

            return list(alternative_slots)

    def save(self, *args, **kwargs):
        """
        Automatically set duration_minutes from the related service.
        """
        if self.service:
            self.duration_minutes = self.service.duration_minutes
        super().save(*args, **kwargs)

class Appointment(models.Model):
    """
    Model to represent an appointment made by a user.
    user, user, available_time, is_confirmed
    """
    user: 'models.ForeignKey' = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )

    available_time = models.ForeignKey(
        'AvailableTime',
        on_delete=models.CASCADE,
        verbose_name=_("Available Time")
    )

    is_confirmed: bool = models.BooleanField(
        default=False,
        verbose_name=_("Is confirmed")
    )

    class Meta:
        verbose_name = _("Appointment")
        verbose_name_plural = _("Appointments")
        unique_together = ("user", "available_time")
    def __str__(self) -> str:
        return f"Appointment for {self.user} at {self.available_time.branch.name} with {self.available_time.provider.full_name} on {self.available_time.start_time} for {self.available_time.service}"

    def confirm_appointment(self) -> None:
        self.is_confirmed = True
        self.save()

    def cancel_appointment(self) -> None:
        self.is_confirmed = False
        self.save()
