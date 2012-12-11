from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
url(r'^gene/$', 'gene.views.index'),
url(r'^gene/fileupload$', 'gene.views.FileUpload'),
url(r'^gene/upload$', 'gene.views.upload'),

    # Examples:
    # url(r'^$', 'geneticanalysis.views.home', name='home'),
    # url(r'^geneticanalysis/', include('geneticanalysis.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns+=staticfiles_urlpatterns()
