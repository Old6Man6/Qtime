from django.urls import path
from .views import UserProfileView, UserRegisterView
from accounts.views import OTPRequestView, OTPVerifyView

urlpatterns = [
    path("", UserProfileView.as_view(), name="user-profile"),
    path("/register", UserRegisterView.as_view(), name="user-register"),
    path("otp/request/", OTPRequestView.as_view(), name="otp_request"),
    path("otp/verify/", OTPVerifyView.as_view(), name="otp_verify"),
]
