from django.urls import path
from .views import LoginView, SignupView, VerifyEmailView, ForgotPasswordView, ResetPasswordView, TestTokenView, TokenRefreshView, logout_view

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset-password'),
    path("auth/test-token/", TestTokenView.as_view(), name="test-token"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
