from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^view/(?P<data_table_id>\w+)$', views.view, name="view"),
    url(r'^analytics/(?P<data_table_id>\w+)$', views.analytics, name="analytics"),
    url(r'^upload_csv/$', views.upload_csv, name='upload_csv'),
    url(r'^export_csv/(?P<data_table_id>\w+)$', views.export_csv, name="export_csv"),
    url(r'^export_xls/(?P<data_table_id>\w+)$', views.export_xls, name="export_xls"),
    url(r'^delete/(?P<data_table_id>\w+)$', views.delete, name="delete"),
]