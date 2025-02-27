from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render

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
            # Login the user
            login(request, user)
            return JsonResponse({"message": "Login successful!"}, status=200)
        else:
            return JsonResponse({"error": "Invalid username or password."}, status=400)
