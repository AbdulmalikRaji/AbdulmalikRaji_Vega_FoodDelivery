from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'role', 'delivery_location', 'latitude', 'longitude', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('longitude', 'latitude')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
