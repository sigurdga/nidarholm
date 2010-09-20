from django.conf.urls.defaults import * #@UnusedWildImport
from django.contrib import admin
from accounts.views import login, logout, register
admin.autodiscover()

from accounts.forms import ProfileForm

urlpatterns = patterns('',
    (r'^login/', login, (), 'login'),
    (r'^logout/', logout, (), 'logout'),
    (r'^register/', register, (), 'register'),
    (r'^forum/', include('nidarholm.forum.urls.debate')),
    (r'^news/', include('nidarholm.news.urls.story')),
    (r'^events/', include('nidarholm.events.urls.event')),
    
    (r'^users/create', 'profiles.views.create_profile', {'form_class': ProfileForm,}),
    (r'^users/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    (r'^users/', include('profiles.urls')),

    (r'^admin/', include(admin.site.urls)),
)
