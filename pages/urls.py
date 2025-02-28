from django.urls import path
from .homepage import homepage
from .login import LoginPageView
from .forgot_password import ForgotPasswordPageView
from .reset_password import ResetPasswordPageView
from .signup import SignupPageView
from .email_verified import EmailVerifiedView
from .menu import MenuPageView
from .menu_item import MenuItemView
from .cart import cart_view, add_to_cart, update_cart, checkout_order

urlpatterns = [
    path('', homepage, name='home'),
    path('login/', LoginPageView.as_view(), name='login-page'),
    path('signup/', SignupPageView.as_view(), name='signup-page'),
    path('email-verified/<uidb64>/<token>/', EmailVerifiedView.as_view(), name='email-verified'),
    path('forgot-password/', ForgotPasswordPageView.as_view(), name='forgot-password-page'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordPageView.as_view(), name='reset-password-page'),
    path('menu/', MenuPageView.as_view(), name='menu-page'),
    path('menu/<int:id>/', MenuItemView.as_view(), name='food-detail'),
    path('add-to-cart/<int:id>/', add_to_cart, name='add-to-cart'),
    path('cart/', cart_view, name='cart-view'),
    path('cart/update/<int:id>/', update_cart, name='update-cart'),
    path('order/checkout/', checkout_order, name='checkout-order'),
]
