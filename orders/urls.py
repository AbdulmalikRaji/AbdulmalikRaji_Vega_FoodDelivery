from django.urls import path
from .views import OrderCreateView, OrderListView, SubmitRatingView

urlpatterns = [
    path('order/', OrderCreateView.as_view(), name='order-create'),
    path('orders/', OrderListView.as_view(), name='my-orders'),
    path('rate-order/', SubmitRatingView.as_view(), name='rate-order')
]
