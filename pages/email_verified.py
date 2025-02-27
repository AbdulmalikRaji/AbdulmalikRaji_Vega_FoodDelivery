from django.shortcuts import render
from django.views import View
import requests

class EmailVerifiedView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        # Send request to VerifyEmailView API
        api_url = request.build_absolute_uri(f'/api/user/verify-email/{uidb64}/{token}/')

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                # Email verified successfully
                success_message = "Your email has been successfully verified. You can now log in."
                return render(request, 'email_verified.html', {
                    'success_message': success_message
                })
            else:
                # Error verifying email
                error_message = response.json().get('error', 'Invalid verification link.')
                return render(request, 'email_verified.html', {
                    'error_message': error_message
                })
        except requests.exceptions.RequestException:
            # Network error
            return render(request, 'email_verified.html', {
                'error_message': 'Network error. Please try again later.'
            })
