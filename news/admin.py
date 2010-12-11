from django.contrib import admin
from news.models import Story

class StoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    fields = ['parent', 'title', 'slug', 'content', 'user', 'group']
    list_display = ('title', 'user', 'group', 'parent')
    list_filter = ('group', 'created')
    ordering = ('-created',)
    search_fields = ('title', 'content_html')

admin.site.register(Story, StoryAdmin)
