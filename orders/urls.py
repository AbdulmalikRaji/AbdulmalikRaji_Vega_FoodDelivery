from django.urls import path
from .views import OrderCreateView

urlpatterns = [
    path('order/', OrderCreateView.as_view(), name='order-create'),
]
