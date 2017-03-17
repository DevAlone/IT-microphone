from django.conf.urls import url

from . import views

fake_admin_regex = r'^admin/$|^wp-admin\.php$|^wp-login.php$|^administrator/$'
fake_admin_regex = r'|^admin.php$'
fake_admin_regex += r'|^bitrix/admin/$|^manager/$'

app_name = 'core'
urlpatterns = [
    url(r'^$', views.eventListView, {'category': 'future'}, name='index'),
    url(r'^events/(?P<category>[a-z]{1,10})/$',
        views.eventListView, name='eventList'),
    # url(r'^event/(?P<pk>[0-9]{1,10})/$', views.EventDetailView.as_view(),
    #    name='event_detail')
    url(r'^event/(?P<pk>[0-9]{1,10})/$', views.eventDetail,
        name='event_detail'),
    url(r'^add/event/', views.addEvent, name='addEvent'),
    url(r'^edit/event/(?P<pk>[0-9]{1,10})/$', views.editEvent,
        name='editEvent'),
    url(fake_admin_regex, views.fakeAdmin, name='fakeAdmin'),
]
