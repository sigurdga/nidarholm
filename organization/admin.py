from django.contrib import admin
from organization.models import GroupCategory, GroupProfile, Role, Membership, SiteProfile

class SiteProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'group', 'admingroup', 'site', 'contact_text')
    list_display = ('site', 'group')
admin.site.register(SiteProfile, SiteProfileAdmin)

admin.site.register(GroupCategory)

class GroupProfileAdmin(admin.ModelAdmin):
    list_display = ('group', 'groupcategory', 'number')
    search_fields = ('group__name',)
    ordering = ('groupcategory', 'number')
admin.site.register(GroupProfile, GroupProfileAdmin)

admin.site.register(Role)
admin.site.register(Membership)
