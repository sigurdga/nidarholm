from django.contrib import admin
from accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'instrument')
    ordering = ('instrument',)

admin.site.register(UserProfile, UserProfileAdmin)
