from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'phone_number',  'is_admin', 'is_staff', 'date_joined')  # Moved name before email
    search_fields = ('email', 'name', 'phone_number')
    list_filter = ('is_staff', 'is_admin', )  # Add filters for admin interface
    ordering = ('-date_joined',)  # Order users by the date joined

admin.site.register(CustomUser, CustomUserAdmin)
