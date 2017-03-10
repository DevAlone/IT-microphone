from django.conf.urls import url

from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^event/(?P<pk>[0-9]{1,10})/$', views.EventDetailView.as_view(),
    #    name='event_detail')
    url(r'^event/(?P<pk>[0-9]{1,10})/$', views.eventDetail,
        name='event_detail')
]
