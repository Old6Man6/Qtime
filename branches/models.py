from django.db import models
from typing import Optional
from django.utils.translation import gettext_lazy as _


class Branch(models.Model):
    """
    Model for branches that offer services.
    """
    name: str = models.CharField(
        max_length=255,
        verbose_name=_("Branch name")
    )

    location: Optional[str] = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Location")
    )

    phone_number: Optional[str] = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name=_("Phone number")
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.location or 'No location'}"


class Service(models.Model):
    """
    Model for services provided by branches (e.g., haircut, massage).
    """
    name: str = models.CharField(
        max_length=255,
        verbose_name=_("Service name")
    )

    description: Optional[str] = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description")
    )

    duration_minutes: int = models.PositiveIntegerField(
        verbose_name=_("Duration (minutes)")
    )

    price: models.DecimalField = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name=_("Price (Toman)"),
        help_text=_("Enter the price in Toman, without decimals")
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.duration_minutes} min"
