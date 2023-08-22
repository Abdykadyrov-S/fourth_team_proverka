from django.contrib import admin

from applications.users.models import User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email']
    list_filter = ['user']


admin.site.register(User)
