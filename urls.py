from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from accounts.views import login, logout, register, groups, group_object_detail, user_groups, member_list
from news.views import story_list
from pages.views import edit_flatpage
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
    r = HttpResponse(intro_text, content_type='text/plain')
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
    (r'^forum/', include('nidarholm.forum.urls')),
    (r'^news/', include('nidarholm.news.urls')),
    (r'^events/', include('nidarholm.events.urls')),
    (r'^files/', include('nidarholm.vault.urls')),

    (r'^sitemap/', include('nidarholm.navigation.urls')),
    #(r'^users/create$', 'profiles.views.create_profile', {'form_class': ProfileForm}),
    (r'^users/edit$', 'profiles.views.edit_profile', {'form_class': ProfileForm}, 'edit-profile'),
    (r'^users/(?P<username>\w+)/groups$', user_groups, (), 'user-groups'),
    (r'^members$', member_list, (), 'member-list'),
    (r'^users/', include('profiles.urls')),
    (r'^groups$', groups, (), 'groups'),
    (r'^groups/(?P<id>\d+)$', group_object_detail, (), 'groups-group'),
    (r'^organization/', include('relations.urls')),

    (r'^pages/(?P<id>\d+)/edit$', edit_flatpage, (), 'edit-flatpage'),
    (r'^admin/', include(admin.site.urls)),
    (r'^avatar/', include('avatar.urls')),
    (r'^urls/', show_url_patterns),
)

if settings.DEVELOPMENT_MODE:
    import os

    urlpatterns += patterns('',
            (r'^m/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
            )

