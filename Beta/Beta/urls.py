from __future__ import unicode_literals

from django.conf.urls import patterns, include, url

from SEADS import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Beta.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.HomePageView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
