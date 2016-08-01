from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^summary/$', views.summary, name='summary'),
    url(r'^upload_csv/$', views.upload_csv, name='upload_csv'),
    url(r'^view/(?P<alpha_or_beta>\w+)$', views.view, name="view_dataset"),
    url(r'^analytics/(?P<alpha_or_beta>\w+)$', views.analytics, name="view_analytics"),
    url(r'^analytics_app/$', views.analytics_app, name="analytics_app"),
    url(r'^export_csv/(?P<alpha_or_beta>\w+)$', views.export_csv, name="export_csv"),
    url(r'^export_xls/(?P<alpha_or_beta>\w+)$', views.export_xls, name="export_xls"),
    url(r'^delete/(?P<alpha_or_beta>\w+)$', views.delete, name="delete"),
]