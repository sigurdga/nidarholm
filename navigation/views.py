from navigation.models import Link
from django.shortcuts import render_to_response

def sitemap(request):
    top_level_links = Link.objects.filter(parent=None)
    return render_to_response('navigation/sitemap.html', {'sitemap': top_level_links})
