from django.contrib.auth import authenticate, login,logout
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
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .utils import reset_password_token
from django.contrib.auth.hashers import make_password
import re


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



def logout_view(request):
    logout(request)
    return redirect('home') 


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
                    reverse('email-verified', kwargs={'uidb64': uid, 'token': token})
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
        
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        try:
            # Get user by email
            user = User.objects.get(email=email)

            # Generate reset link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = reset_password_token.make_token(user)
            reset_link = request.build_absolute_uri(
                reverse('reset-password-page', kwargs={'uidb64': uid, 'token': token})
            )

            # Send reset email
            send_mail(
                subject='Reset Your Password',
                message=f'Click the link to reset password for user @{user.username}: {reset_link}',
                from_email='no-reply@fooddelivery.com',
                recipient_list=[user.email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link sent!"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, uidb64, token):
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # Check password requirements
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)', new_password):
            return Response({
                "error": "Password must have at least one uppercase letter, one lowercase letter, and one number."
            }, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode user ID and get user object
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=uid)

            # Check the token
            if reset_password_token.check_token(user, token):
                # Set new password and save
                user.password = make_password(new_password)
                user.save()

                return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)