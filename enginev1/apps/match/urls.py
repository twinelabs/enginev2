from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^summary/$', views.summary, name='summary'),
    url(r'^create_match/$', views.create_match, name='create_match'),
    url(r'^view/(?P<config_id>\w+)$', views.view, name="view"),
    url(r'^delete_match/(?P<config_id>\w+)$', views.delete_match, name="delete_match"),
    url(r'^delete_result/(?P<config_id>\w+)/(?P<result_id>\w+)$', views.delete_result, name="delete_result"),
    url(r'^run_match/(?P<config_id>\w+)$', views.run_match, name="run_match"),
]