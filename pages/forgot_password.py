from django.shortcuts import render
from django.views import View
import requests
from django.conf import settings

class ForgotPasswordPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'forgot_password.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        # Send POST request to your existing API endpoint
        api_url = request.build_absolute_uri('/api/user/forgot-password/')
        payload = {'email': email}
        try:
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                # Success - Show success message
                return render(request, 'forgot_password.html', {
                    'success_message': 'Password reset link sent! Check your email.'
                })
            else:
                # Error from API - Show error message
                error_message = response.json().get('error', 'Something went wrong.')
                return render(request, 'forgot_password.html', {
                    'error_message': error_message
                })
        except requests.exceptions.RequestException as e:
            # Network error
            return render(request, 'forgot_password.html', {
                'error_message': 'Network error. Please try again later.'
            })
