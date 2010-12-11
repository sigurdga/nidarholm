from django.contrib import admin
from vault.models import UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'user', 'group')
    list_filter = ('group', 'uploaded')
    ordering = ('-uploaded',)
    search_fields = ('filename', 'content_html')


admin.site.register(UploadedFile, UploadedFileAdmin)

