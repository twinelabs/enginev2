from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^summary/$', views.summary, name='summary'),
    url(r'^viewA/$', views.viewA, name='viewA'),
    url(r'^viewB/$', views.viewB, name='viewB'),
]