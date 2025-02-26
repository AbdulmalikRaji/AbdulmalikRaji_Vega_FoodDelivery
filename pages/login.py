from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
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
            return redirect('home')  # Redirect to homepage after login
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login-page') # Redirect to login page
