from django.urls.conf import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView



urlpatterns = [
    path('admin/', admin.site.urls),

    # API apps
    path('api/', include('appointments.urls')),
    path('api/', include('branches.urls')),
    path('api/accounts', include('accounts.urls')),

    # JWT authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Schema / Documentation
    path('schema/', SpectacularAPIView.as_view(), name="schema"),
    path('swagger/', SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('redoc/', SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


# if settings.USE_OTP_LOGIN:
#     urlpatterns += [
#         path('otp/request/', OTPRequestView.as_view(), name='otp-request'),
#         path('otp/verify/', OTPVerifyView.as_view(), name='otp-verify'),
#     ]