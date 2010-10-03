from django.conf.urls.defaults import * #@UnusedWildImport
from django.contrib import admin
from accounts.views import login, logout, register
from news.views import story_list
admin.autodiscover()

from accounts.forms import ProfileForm

from django.core import urlresolvers
from django.http import HttpResponse

intro_text = """Named URL patterns for the {% url %} tag
========================================

e.g. {% url pattern-name %}
or   {% url pattern-name arg1 %} if the pattern requires arguments

"""
def show_url_patterns(request):
    patterns = _get_named_patterns()
    r = HttpResponse(intro_text, content_type = 'text/plain')
    longest = max([len(pair[0]) for pair in patterns])
    for key, value in patterns:
        r.write('%s %s\n' % (key.ljust(longest + 1), value))
    return r

def _get_named_patterns():
    "Returns list of (pattern-name, pattern) tuples"
    resolver = urlresolvers.get_resolver(None)
    patterns = sorted([
        (key, value[0][0][0])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, basestring)
    ])
    return patterns



urlpatterns = patterns('',
    (r'^$', story_list, (), 'main'),
    (r'^login/', login, (), 'login'),
    (r'^logout/', logout, (), 'logout'),
    (r'^register/', register, (), 'register'),
    (r'^forum/', include('nidarholm.forum.urls.debate')),
    (r'^news/', include('nidarholm.news.urls.story')),
    (r'^events/', include('nidarholm.events.urls.event')),
    (r'^files/', include('nidarholm.vault.urls.uploadedfile')),
    
    (r'^sitemap/', include('nidarholm.navigation.urls.sitemap')),
    (r'^users/create', 'profiles.views.create_profile', {'form_class': ProfileForm,}),
    (r'^users/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    (r'^users/', include('profiles.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^urls/', show_url_patterns)
)

