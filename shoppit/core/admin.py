from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'city', 'state', 'address', 'phone', 'is_staff', 'is_active'),
        }),
    )
    # You can add list_display and search_fields for better admin usability
    # list_display = ('username', 'email', 'city', 'state', 'is_staff')
    # search_fields = ('username', 'email', 'city', 'state')
admin.site.register(CustomUser, CustomUserAdmin)
