from django.conf.urls import url

from . import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.eventListView, {'category':'future'}, name='index'),
    url(r'^events/(?P<category>[a-z]{1,10})/$',
        views.eventListView, name='eventList'),
    # url(r'^event/(?P<pk>[0-9]{1,10})/$', views.EventDetailView.as_view(),
    #    name='event_detail')
    url(r'^event/(?P<pk>[0-9]{1,10})/$', views.eventDetail,
        name='event_detail'),
    url(r'add/event/', views.addEvent, name='addEvent'),
    url(r'test/', views.test, name='test'),
]
