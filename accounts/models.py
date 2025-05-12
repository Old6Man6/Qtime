from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from typing import Optional
import os


# Validators
phone_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message=_("Phone number must start with 09 and be exactly 11 digits.")
)

email_validator = EmailValidator(
    message=_("Enter a valid email address.")
)

full_name_validator = RegexValidator(
    regex=r'^[a-zA-Z\u0600-\u06FF\s]+$',
    message=_("Full name can only contain Persian or English letters and spaces.")
)


def profile_image_path(instance: 'User', filename: str) -> str:
    """
    Generate file path for storing user profile images.
    """
    folder_name = f"{instance.id}-{instance.phone}"
    return os.path.join("profiles", folder_name, filename)


class UserManager(BaseUserManager):
    """
    Custom manager to handle user creation and superuser creation.
    """

    def create_user(self, phone: str, password: Optional[str] = None, **extra_fields) -> 'User':
        """
        Create and return a regular user with a phone number and password.
        """
        if not phone:
            raise ValueError(_("Phone number is required"))

        user = self.model(phone=phone, **extra_fields)

        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, phone: str, password: str, **extra_fields) -> 'User':
        """
        Create and return a superuser with a phone number and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model extending AbstractBaseUser to include phone, email, name, role, etc.
    """

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('provider', 'provider')
    )

    phone: str = models.CharField(
        max_length=11,
        unique=True,
        db_index=True,
        validators=[phone_validator],
        verbose_name=_("Phone")
    )

    email: Optional[str] = models.EmailField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,
        validators=[email_validator],
        verbose_name=_("Email")
    )

    full_name: Optional[str] = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        validators=[full_name_validator],
        verbose_name=_("Name")
    )

    avatar: Optional[models.ImageField] = models.ImageField(
        upload_to=profile_image_path,
        null=True,
        blank=True,
        verbose_name=_("Avatar")
    )

    role: str = models.CharField(
        max_length=8,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name=_("Role")
    )

    is_active: bool = models.BooleanField(default=True)
    is_staff: bool = models.BooleanField(default=False)

    ip_address: Optional[str] = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    objects: UserManager = UserManager()

    USERNAME_FIELD: str = 'phone'
    REQUIRED_FIELDS: list = []  # Email is optional

    def __str__(self) -> str:
        """
        Return a string representation of the user, including their phone number and role.
        """
        return f"{self.phone} ({self.role})"
