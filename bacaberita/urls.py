from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^bacaberita/', include('bacaberita.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

	(r'^news/update', 'bacaberita.news.views.update'),
	(r'^$', 'bacaberita.news.views.index'),
	(r'^read/$', 'bacaberita.news.views.read'),
	(r'^read/(cat|feed)/(.+)?$', 'bacaberita.news.views.read'),
	(r'^json/$', 'bacaberita.news.views.json'),
	(r'^json/(cat|feed)/(.+)?$', 'bacaberita.news.views.json'),
)
