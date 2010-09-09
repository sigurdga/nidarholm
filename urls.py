from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^forum/', include('nidarholm.forum.urls.debate')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
