from django.shortcuts import render, redirect
from django.views import View
import requests

class ResetPasswordPageView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        # Render the form for new password input
        return render(request, 'reset_password.html', {
            'uidb64': uidb64,
            'token': token
        })

    def post(self, request, uidb64, token, *args, **kwargs):
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Send POST request to API endpoint
        api_url = request.build_absolute_uri(f'/api/user/reset-password/{uidb64}/{token}/')
        payload = {
            'new_password': new_password,
            'confirm_password': confirm_password
        }
        
        try:
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                # Success - Show success message and redirect to login
                return render(request, 'reset_password.html', {
                    'success_message': 'Password reset successful! Redirecting to login...',
                    'redirect_url': 'login-page'
                })

            else:
                # Error from API - Show error message
                error_message = response.json().get('error', 'Something went wrong.')
                return render(request, 'reset_password.html', {
                    'error_message': error_message,
                    'uidb64': uidb64,
                    'token': token
                })
        
        except requests.exceptions.RequestException:
            # Network error
            return render(request, 'reset_password.html', {
                'error_message': 'Network error. Please try again later.',
                'uidb64': uidb64,
                'token': token
            })
