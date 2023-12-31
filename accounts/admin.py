from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.
from accounts.models import CustomUser

class UserAdmin(BaseUserAdmin):
  model = CustomUser

  list_display = ('email', 'username', 'is_active')
  list_filter = ('is_active', 'is_staff', 'is_superuser')
  fieldsets = (
      (None, {'fields': ('username', 'email', 'password')}),
      ('Permissions', {'fields': ('is_staff', 'is_active',
        'is_superuser', 'groups', 'user_permissions')}),
      ('Dates', {'fields': ('last_login', 'date_joined')})
  )
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
  )
  search_fields = ('email',)
  ordering = ('email',)

admin.site.register(CustomUser, UserAdmin)