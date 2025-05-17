import django_filters
from .models import AvailableTime

class AvailableTimeFilter(django_filters.FilterSet):
    """
    Filter for AvailableTime based on provider, branch, service, and start time range.
    """
    start = django_filters.IsoDateTimeFilter(field_name="start_time", lookup_expr='gte')
    end = django_filters.IsoDateTimeFilter(field_name="start_time", lookup_expr='lte')

    class Meta:
        model = AvailableTime
        fields = ['branch', 'provider', 'service', 'start', 'end']
