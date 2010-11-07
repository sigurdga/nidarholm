from django import template
from vault.models import UploadedFile

register = template.Library()

@register.simple_tag
def file_list(request, count=10):
    files = UploadedFile.objects.for_user(request.user)[0:count]
    return html_list(files)

def html_list(list):
    ret = "<ul>"
    for file in list:
        ret += "<li><a href=\"" + file.get_absolute_url() + "\">" + file.filename + "</a></li>"
    ret += "</ul>"
    return ret
