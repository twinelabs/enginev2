from django.conf.urls import include, url
from django.contrib import admin

from enginev1.apps.welcome import urls as welcome_urls
from enginev1.apps.dataset import urls as dataset_urls
from enginev1.apps.match import urls as match_urls

from enginev1.apps.welcome import views as welcome_views

urlpatterns = [
    url(r'^welcome/', include(welcome_urls)),
    url(r'^dataset/', include(dataset_urls)),
    url(r'^match/', include(match_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', welcome_views.user_login)
]
