from django.conf.urls import url

from . import views

fake_admin_regex = r'^admin/$|^wp-admin\.php$|^wp-login\.php$|^administrator/$'
fake_admin_regex += r'|^admin.php$'
fake_admin_regex += r'|^bitrix/admin/$|^manager/$'

app_name = 'core'
urlpatterns = [
    url(fake_admin_regex, views.fakeAdmin, name='fakeAdmin'),
]
