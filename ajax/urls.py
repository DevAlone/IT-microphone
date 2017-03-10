from django.conf.urls import url

from . import views

app_name = 'ajax'
urlpatterns = [
        url(r'^eventSubscribe/(?P<pk>[0-9]{1,10})/$', views.eventSubscribe,
            name='event-subscribe'),

        url(r'^eventUnsubscribe/(?P<pk>[0-9]{1,10})/$', views.eventUnsubscribe,
            name='event-unsubscribe'),
]
