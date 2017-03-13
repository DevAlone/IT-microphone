from django.conf.urls import url
from django.contrib.auth.views import login, logout, password_change
from django.views.generic import TemplateView

from . import views

app_name = 'accounts'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<username>[a-zA-Z0-9_]{1,30})/$', views.profile,
        name='profile'),
    url(r'^edit/profile/$', views.editProfile, name='editProfile'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^change/password/$', password_change,
        {'template_name': 'accounts/change_password.html',
         'post_change_redirect': 'accounts:changePasswordDone'},
        name='changePassword'),
    url(r'^change/password/done/$',
        TemplateView.as_view(template_name='accounts/change_password_done.html'),
        name='changePasswordDone'),
]
