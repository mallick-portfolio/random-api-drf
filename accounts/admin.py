from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from accounts.models import CustomUser

class UserAdmin(BaseUserAdmin):
  model = CustomUser

  list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_superuser')
  list_filter = ('is_active', 'is_staff', 'is_superuser')
  fieldsets = (
      (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'phone', 'gender', 'otp',)}),
      ('Permissions', {'fields': ('is_staff', 'is_active','is_email_verified',
        'is_superuser', 'groups', 'user_permissions', )}),
      ('Dates', {'fields': ('otp_created_at', 'last_login', 'date_joined')})
  )

  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('email','first_name', 'last_name', 'phone', 'gender', 'otp', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
  )
  search_fields = ('email',)
  ordering = ('email',)
  readonly_fields = ['otp_created_at']

admin.site.register(CustomUser, UserAdmin)