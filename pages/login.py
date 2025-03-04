from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken

class LoginPageView(View):
    def get(self, request):
        # Render the login template on GET request
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user.is_verified)
            if user.is_verified == False:
                return JsonResponse({"error": "User email is not verified"}, status=401)
            # Login the user
            login(request, user)
            refresh = RefreshToken.for_user(user)
            request.session['access_token'] = str(refresh.access_token)
            request.session['refresh_token'] = str(refresh)
            return JsonResponse({"message": "Login successful!"}, status=200)
        else:
            return JsonResponse({"error": "Invalid username or password."}, status=400)
