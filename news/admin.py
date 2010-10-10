from django.contrib import admin
from news.models import Story
from permissions.admin import ObjectPermissionMixin, ObjectPermissionInline

class StoryAdmin(ObjectPermissionMixin, admin.ModelAdmin):
    #inlines = [ObjectPermissionInline]
    prepopulated_fields = {"slug": ("title",)}
    fields = ['parent', 'title', 'slug', 'text', 'user', 'group']

admin.site.register(Story, StoryAdmin)
