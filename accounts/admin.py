from django.contrib import admin
from accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'born', 'joined')
    ordering = ('user',)
    list_filter = ('status',)
admin.site.register(UserProfile, UserProfileAdmin)

