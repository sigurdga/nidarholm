from django.contrib import admin
from organization.models import GroupCategory, GroupProfile, Role, Membership, SiteProfile

admin.site.register(GroupCategory)
admin.site.register(GroupProfile)
admin.site.register(Role)
admin.site.register(Membership)
admin.site.register(SiteProfile)