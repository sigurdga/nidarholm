from django.contrib import admin, messages
from vault.models import UploadedFile
from permissions.admin import ObjectPermissionMixin, ObjectPermissionInline
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class UploadedFileAdmin(ObjectPermissionMixin, admin.ModelAdmin):
    inlines = [ObjectPermissionInline]
    
    def change_view(self, request, *args, **kwargs):
        try:
            return super(UploadedFileAdmin, self).change_view(request, *args, **kwargs)
        except PermissionDenied, e:
            messages.add_message(request, messages.ERROR, u"You don't have the necessary permissions!")
            return HttpResponseRedirect(reverse('admin:flatpages_flatpage_changelist'))

admin.site.register(UploadedFile, UploadedFileAdmin)