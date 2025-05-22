from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from .serializers import UserProfileSerializer, UserRegisterSerializer
from django.utils.translation import gettext_lazy as _
"""===========OTP imports==========="""
from accounts.serializers import OTPRequestSerializer, OTPVerifySerializer
from django.conf import settings
from accounts.utils.otp import (
    generate_otp_code,
    set_otp_code,
    get_otp_code,
    delete_otp_code,
    is_rate_limited,
    set_rate_limit
)
from accounts.services.sms import send_otp_sms
from accounts.models import User
"""============END OTP imports==========="""
class UserProfileView(APIView):
    """
    View for retrieving and updating the authenticated user's profile.

    Only authenticated users can access this view.
    Users can only update editable fields such as full_name, email, and avatar.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return the profile data of the authenticated user.
        """
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """
        Partially update the profile of the authenticated user.
        """
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": _("User registered successfully.")},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class OTPRequestView(APIView):
    """
    Request OTP code to be sent to the user's phone.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if not settings.OTP_LOGIN_ENABLED:
            return Response({"detail": "OTP login is disabled."}, status=403)

        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data['phone']

        if is_rate_limited(phone):
            return Response({"detail": "Please wait before requesting another code."}, status=429)

        code = generate_otp_code()
        set_otp_code(phone, code)
        set_rate_limit(phone)
        send_otp_sms(phone, code)

        return Response({"detail": _("OTP code sent successfully.")}, status=200)




"""====================OTP SECTION===================="""
class OTPVerifyView(APIView):
    """
    Verify the provided OTP code and log the user in.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if not settings.OTP_LOGIN_ENABLED:
            return Response({"detail": "OTP login is disabled."}, status=403)

        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        input_code = serializer.validated_data['code']
        actual_code = get_otp_code(phone)

        if input_code != actual_code:
            return Response({"detail": "Invalid or expired OTP code."}, status=400)

        user, created = User.objects.get_or_create(phone=phone)
        delete_otp_code(phone)

        from rest_framework_simplejwt.tokens import RefreshToken
        tokens = RefreshToken.for_user(user)

        return Response({
            "refresh": str(tokens),
            "access": str(tokens.access_token),
        }, status=200)
