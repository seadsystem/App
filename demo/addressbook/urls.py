from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import contacts.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'addressbook.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', contacts.views.ListcontactView.as_view(),
        name='contacts-list',),
    url(r'^new$', contacts.views.CreatecontactView.as_view(),
    	name='contacts-new',),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^/$', contacts.views.IndexView.as_view()),
)

urlpatterns += staticfiles_urlpatterns()