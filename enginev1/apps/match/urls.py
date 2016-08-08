from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$', views.create, name='create'),
    url(r'^view/(?P<match_id>\w+)$', views.view, name="view"),
    url(r'^analyze/(?P<match_id>\w+)$', views.analyze, name="analyze"),
    url(r'^run/(?P<match_id>\w+)$', views.run, name="run"),
    url(r'^delete/(?P<match_id>\w+)$', views.delete, name="delete"),
]