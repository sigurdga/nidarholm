from django.contrib import admin
from news.models import Story
from permissions.admin import ObjectPermissionMixin, ObjectPermissionInline

class StoryAdmin(ObjectPermissionMixin, admin.ModelAdmin):
    inlines = [ObjectPermissionInline]
    fields = ['parent', 'title', 'slug', 'content_markdown']

admin.site.register(Story, StoryAdmin)
