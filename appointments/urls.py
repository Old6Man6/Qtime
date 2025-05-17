from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.UserAppointmentView.as_view(), name='user-appointments'),
    path('appointments/admin/', views.AdminAppointmentListView.as_view(), name='admin-appointments'),
    path('appointments/provider/', views.ProviderAppointmentListView.as_view(), name='provider-appointments'),
    path('appointments/<int:pk>/delete/', views.ProviderAppointmentDeleteView.as_view(), name='provider-delete-appointment'),
    path('available-times/', views.AvailableTimeListView.as_view(), name='available-times'),

]
