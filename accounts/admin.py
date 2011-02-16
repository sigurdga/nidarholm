from django.contrib import admin
from accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'born', 'joined')
    ordering = ('user',)
    list_filter = ('status',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
admin.site.register(UserProfile, UserProfileAdmin)

