from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from accounts.forms import ProfileForm

urlpatterns = patterns('',
    (r'^forum/', include('nidarholm.forum.urls.debate')),
    (r'^news/', include('nidarholm.news.urls.story')),
    
    (r'^users/create', 'profiles.views.create_profile', {'form_class': ProfileForm,}),
    (r'^users/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    (r'^users/', include('profiles.urls')),

    (r'^admin/', include(admin.site.urls)),
)
