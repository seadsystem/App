from django.conf.urls import patterns, include, url
from django.contrib import admin
from seadssite import views as v
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SeadsFront.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', v.IndexView.as_view()),
    url(r'^visualization/', v.VisualizationView),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout',
    	{'next_page': '/'}),
    url(r'^register/$', v.register),
)

urlpatterns += staticfiles_urlpatterns()