from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', include('quotedb.urls', namespace='quotedb')),
	url(r'^qdb/', include('quotedb.urls', namespace='quotedb')),
	url(r'^admin/', include(admin.site.urls)),
) 

