from django.contrib import admin
from organization.models import GroupCategory, GroupProfile, Role, Membership, SiteProfile

class SiteProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'group', 'site', 'contact_text')
    list_display = ('site', 'group')
admin.site.register(SiteProfile, SiteProfileAdmin)

admin.site.register(GroupCategory)
admin.site.register(GroupProfile)
admin.site.register(Role)
admin.site.register(Membership)
