from django.contrib import admin
from vault.models import UploadedFile

class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('filename', 'tags', 'user', 'group')
    list_filter = ('group', 'uploaded')
    ordering = ('-uploaded',)
    search_fields = ('filename', 'tags')


admin.site.register(UploadedFile, UploadedFileAdmin)

