from django.urls import path
from .homepage import homepage
from .login import LoginPageView

urlpatterns = [
    path('', homepage, name='home'),
    path('login/', LoginPageView.as_view(), name='login-page'),
]
