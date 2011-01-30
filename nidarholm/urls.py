from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from accounts.views import groups, group_object_detail, user_groups, member_list, edit_profile, new_profile
from news.views import story_list
from pages.views import edit_flatpage, new_flatpage, flatpage_list
from accounts.forms import ProfileForm, LoginForm

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', story_list, (), 'main'),
    (r'^accounts/login/', 'django.contrib.auth.views.login', {'authentication_form': LoginForm}, 'auth_login'),
    (r'^accounts/', include('registration.urls')),
    (r'^forum/', include('forum.urls')),
    (r'^news/', include('news.urls')),
    (r'^events/', include('events.urls')),
    (r'^projects/', include('projects.urls')),
    (r'^files/', include('vault.urls')),

    (r'^sitemap/', include('navigation.urls')),
    (r'^users/new/$', new_profile, (), 'new-profile'),
    (r'^users/(?P<id>\d+)/edit/$', edit_profile, (), 'edit-profile'),
    #(r'^users/new/$', 'profiles.views.create_profile', {'form_class': ProfileForm}, 'create-profile'),
    (r'^users/(?P<username>\w+)/groups$', user_groups, (), 'user-groups'),
    (r'^members$', member_list, (), 'member-list'),
    (r'^users/', include('profiles.urls')),
    (r'^groups$', groups, (), 'groups'),
    (r'^groups/(?P<id>\d+)$', group_object_detail, (), 'groups-group'),
    (r'^organization/', include('organization.urls')),

    (r'^pages/(?P<id>\d+)/edit$', edit_flatpage, (), 'edit-flatpage'),
    (r'^pages/new$', new_flatpage, (), 'new-flatpage'),
    (r'^pages/$', flatpage_list, (), 'flatpage-list'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^avatar/', include('avatar.urls')),
    (r'^search/', include('search.urls')),
)

if settings.DEVELOPMENT_MODE:
    import os

    urlpatterns += patterns('',
            (r'^m/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.abspath(os.path.dirname(__file__)), 'media')}),
            )

