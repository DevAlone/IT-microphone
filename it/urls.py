"""it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views import static
# from django.conf import settings
from . import settings

urlpatterns = i18n_patterns(
    url(r'^', include('core.urls')),
    url(r'^ajax/', include('ajax.urls')),
    url(r'ajax/chat/', include('chat.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^adminthissite214243214/', admin.site.urls),
)

urlpatterns += [url(r'^', include('fakeadmin.urls')), ]
if settings.DEBUG:
    urlpatterns += i18n_patterns(
        url(r'^media/(?P<path>.*)$', static.serve, {
            'document_root': settings.MEDIA_ROOT
        })
    )
