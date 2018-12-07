from django.contrib import admin
from Fydlyty2.accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserProfile, UserProfileAdmin)
