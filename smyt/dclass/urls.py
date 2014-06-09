from django.conf.urls import patterns, url
from dclass import views

urlpatterns = patterns('',
                       url(r'^(?P<model>\w+)/(?P<pk>[0-9]+)/$', views.ModelDetails.as_view()),
                       url(r'^(?P<model>\w+)/$', views.Model.as_view()),
                       url(r'^$', views.ModelList.as_view()),

    )
