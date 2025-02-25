from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer
from django.core.mail import send_mail
from django.db import transaction
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .utils import email_verification_token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()

class LoginView(APIView):
    permission_classes = [AllowAny]  # Allow public access
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in for session authentication
            login(request, user)

            # Create JWT tokens for API access
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "Login successful!",
                "access_token": access_token,
                "refresh_token": str(refresh)
            })
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Create user within a transaction
                user = serializer.save()

                # Send verification email
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = email_verification_token.make_token(user)
                verification_link = request.build_absolute_uri(
                    reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
                )

                send_mail(
                    subject='Verify Your Email',
                    message=f'Click the link to verify your email: {verification_link}',
                    from_email='dfood1986@gmail.com',
                    recipient_list=[user.email],
                    fail_silently=False,  # IMPORTANT: Fail explicitly
                )

                return Response({
                    "message": "Signup successful! Check your email to verify your account."
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                # If email fails, rollback the user creation
                transaction.set_rollback(True)
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)

            # Check the token
            if email_verification_token.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Invalid verification link."}, status=status.HTTP_400_BAD_REQUEST)