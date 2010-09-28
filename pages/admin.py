from django import forms
from django.contrib import admin
from permissions.admin import ObjectPermissionInline, ObjectPermissionMixin
from pages.models import FlatPage
#from django.contrib.flatpages.admin import FlatPageAdmin as FPAdmin
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse

class FlatpageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " underscores, dashes or slashes."))

    class Meta:
        model = FlatPage


class FlatPageAdmin(ObjectPermissionMixin, admin.ModelAdmin):
    form = FlatpageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content_markdown', 'sites')}),
        #(_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),
    )
    list_display = ('url', 'title')
    #list_filter = ('sites', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')
    inlines = [ObjectPermissionInline]
    
    def change_view(self, request, *args, **kwargs):
        try:
            return super(FlatPageAdmin, self).change_view(request, *args, **kwargs)
        except PermissionDenied, e:
            messages.add_message(request, messages.ERROR, u"You don't have the necessary permissions!")
            return HttpResponseRedirect(reverse('admin:flatpages_flatpage_changelist'))

admin.site.register(FlatPage, FlatPageAdmin)
