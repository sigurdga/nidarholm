from django.contrib import admin
from news.models import Story

class StoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fields = ['parent', 'title', 'slug', 'text', 'user', 'group']

admin.site.register(Story, StoryAdmin)
