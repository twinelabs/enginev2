from django.conf.urls import include, url
from django.contrib import admin

from enginev1.apps.welcome import urls as welcome_urls

urlpatterns = [
    url(r'^welcome/', include(welcome_urls)),
    url(r'^admin/', include(admin.site.urls)),
]
