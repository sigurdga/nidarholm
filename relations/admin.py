from django.contrib import admin
from relations.models import GroupCategory, GroupProfile, Role, Membership

admin.site.register(GroupCategory)
admin.site.register(GroupProfile)
admin.site.register(Role)
admin.site.register(Membership)
