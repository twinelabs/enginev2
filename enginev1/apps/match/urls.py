from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^feedback/$', views.feedback, name='feedback'),
    url(r'^create/$', views.create, name='create'),
    url(r'^create_custom/$', views.create_custom, name='create_custom'),
    url(r'^view/(?P<match_id>\w+)$', views.view, name="view"),
    url(r'^analyze/(?P<match_id>\w+)$', views.analyze, name="analyze"),
    url(r'^run/(?P<match_id>\w+)$', views.run, name="run"),
    url(r'^delete/(?P<match_id>\w+)$', views.delete, name="delete"),
]