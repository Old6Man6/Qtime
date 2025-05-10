from django.db import models
from typing import Optional
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """
    Model for storing notifications for users.
    """
    user: 'models.ForeignKey' = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )

    message: str = models.CharField(
        max_length=255,
        verbose_name=_("Message")
    )

    sent_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Sent at")
    )

    is_read: bool = models.BooleanField(
        default=False,
        verbose_name=_("Is read")
    )

    def __str__(self) -> str:
        """
        Return a string representation of the notification.
        """
        return f"Notification for {self.user} at {self.sent_at}"
