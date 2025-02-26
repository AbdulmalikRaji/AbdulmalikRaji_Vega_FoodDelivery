from django.urls import path
from .homepage import homepage

urlpatterns = [
    path('', homepage, name='homepage'),
]
