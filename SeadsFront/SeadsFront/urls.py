from django.conf.urls import patterns, include, url
from django.contrib import admin
from seadssite import views as v
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#both added for blog

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', v.IndexView.as_view()),
    url(r'^dashboard/',v.DashboardView),
    url(r'^visualization/([0-9]*)/$', v.VisualizationView),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout',
    	{'next_page': '/'}),
    url(r'^register/$', v.register),
    url(r'^WeeklyNews/$', v.WeeklyNews),
    url(r'^seadssite/WeeklyNews/view/(?P<slug>[^\.]+).html','seadssite.views.view_post', name='view_blog_post'),
    url(r'^seadssite/WeeklyNews/category/(?P<slug>[^\.]+).html','seadssite.views.view_category', name='view_blog_category'),
    # url(r'^post/new/$', v.WeeklyNews),
    url(r'^seadssite/postnew/$', 'seadssite.views.post_new', name="new_post"),

)                    

urlpatterns += staticfiles_urlpatterns()