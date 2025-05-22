from django.contrib import admin
from .models import Branch, Service
from appointments.models import AvailableTime
from django.utils.translation import gettext_lazy as _


class AvailableTimeInline(admin.TabularInline):
    model = AvailableTime
    extra = 0
    fields = ('provider', 'service', 'start_time', 'duration_minutes', 'is_booked')
    readonly_fields = ('is_booked',)
    show_change_link = True
    verbose_name = _("Available Time")
    verbose_name_plural = _("Available Times")
    ordering = ('-start_time',)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'phone_number')
    search_fields = ('name', 'location', 'phone_number')
    inlines = [AvailableTimeInline]


class ServiceInline(admin.TabularInline):
    model = Service
    extra = 0
    fields = ('name', 'duration_minutes', 'price', 'description')