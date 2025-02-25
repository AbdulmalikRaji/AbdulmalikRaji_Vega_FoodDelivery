from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer


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
    permission_classes = [AllowAny]  # Allow public access
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            
            # Specify the backend explicitly
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            # Log the user in
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Create JWT tokens for API access
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "Signup successful!",
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
