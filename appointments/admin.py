from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Appointment, AvailableTime


@admin.action(description=_("Confirm selected appointments"))
def confirm_appointments(modeladmin, request, queryset):
    updated = queryset.update(is_confirmed=True)
    modeladmin.message_user(request, _("%d appointment(s) confirmed." % updated))


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'provider', 'service', 'branch', 'start_time', 'is_confirmed')
    list_filter = ('is_confirmed', 'available_time__provider', 'available_time__branch')
    search_fields = ('user__phone', 'available_time__provider__phone')
    list_select_related = ('available_time', 'user')
    actions = [confirm_appointments]  # ← Action for bulk confirming

    @admin.display(ordering='available_time__start_time', description=_("Start Time"))
    def start_time(self, obj):
        return obj.available_time.start_time

    @admin.display(description=_("Provider"))
    def provider(self, obj):
        return obj.available_time.provider.full_name or obj.available_time.provider.phone

    @admin.display(description=_("Service"))
    def service(self, obj):
        return obj.available_time.service.name

    @admin.display(description=_("Branch"))
    def branch(self, obj):
        return obj.available_time.branch.name
