from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^summary/$', views.summary, name='summary'),
    url(r'^upload_csv/$', views.upload_csv, name='upload_csv'),
    url(r'^view/(?P<alpha_or_beta>\w+)$', views.view, name="view_dataset"),
    url(r'^delete/(?P<alpha_or_beta>\w+)$', views.delete, name="delete"),
]