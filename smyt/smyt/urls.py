from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'smyt.views.home', name='home'),
    url(r'^api/', include('dclass.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'',  RedirectView.as_view(url='/static/index.html')),
)
