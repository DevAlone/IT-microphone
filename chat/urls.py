from django.conf.urls import url
from . import views


app_name = 'chat'
urlpatterns = [
    url(r'^(?P<pk>[0-9]{1,10})/messages/$', views.getMessages,
        name='getMessages'),
#    url(r'^$', views.eventListView, {'category': 'future'}, name='index'),
#    url(r'^event/(?P<pk>[0-9]{1,10})/$', views.eventDetail,
#        name='event_detail'),
]
