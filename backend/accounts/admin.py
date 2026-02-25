from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'role', 'is_active', 'is_staff', 'date_joined')  # direct fields
    search_fields = ('email',)
    list_filter = ('role', 'is_active', 'is_staff')
    ordering = ('email',)

    
    @admin.display(description='User')
    def user_info(self, obj):
         return f"{obj.email} ({obj.role})"
