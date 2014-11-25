from django.conf.urls import patterns, include, url
from django.contrib import admin
from seadssite import views as v
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', v.IndexView.as_view()),
    url(r'^devices/',v.DevicesView),
    url(r'^dashboard/',v.DashboardView),
    url(r'^visualization/([0-9]*)/$', v.VisualizationView),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout',
    	{'next_page': '/'}),
    url(r'^register/$', v.register),
    url(r'^help/$', v.help),
    url(r'^$', v.reset),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            v.reset_confirm),
    url(r'^success/$', v.success),

                        )

urlpatterns += staticfiles_urlpatterns()