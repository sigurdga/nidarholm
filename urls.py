from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^forum/', include('nidarholm.forum.urls.debate')),
    (r'^news/', include('nidarholm.news.urls.story')),

    (r'^admin/', include(admin.site.urls)),
)
