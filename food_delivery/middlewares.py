from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
import requests

class RefreshTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip middleware for API login, logout, and token refresh endpoints
        if request.path in ["/api/user/auth/login/", "/api/user/auth/logout/", "/api/user/auth/token/refresh/"]:
            return None
        
        access_token = request.session.get("access_token")
        refresh_token = request.session.get("refresh_token")

        # If no access token, do nothing (don't refresh)
        if not access_token:
            return None  

        # Test if the token is valid
        test_response = requests.get(
            f"{settings.API_BASE_URL}/api/user/auth/test-token/",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        if test_response.status_code == 200:
            return None  # Token is valid, proceed normally

        elif test_response.status_code == 401 and refresh_token:
            # Try refreshing the token
            refresh_response = requests.post(
                f"{settings.API_BASE_URL}/api/user/auth/token/refresh/",
                json={"refresh": refresh_token},
            )

            if refresh_response.status_code == 200:
                new_tokens = refresh_response.json()
                request.session["access_token"] = new_tokens["access"]
                return None  # Token successfully refreshed

            else:
                # If refresh fails, clear session and redirect to login
                request.session.flush()
                return redirect("/login/")

        return None  # Default case: do nothing
