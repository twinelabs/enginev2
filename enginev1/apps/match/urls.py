from django.conf.urls import url

from . import views, views_ajax

urlpatterns = [

    url(r'^create_group/$', views.create_group, name='create_group'),
    url(r'^create_assign/$', views.create_assign, name='create_assign'),
    url(r'^create_employeerole/$', views.create_employeerole, name='create_employeerole'),
    url(r'^view/(?P<match_id>\w+)$', views.view, name="view"),
    url(r'^analyze/(?P<match_id>\w+)$', views.analyze, name="analyze"),
    url(r'^feedback/(?P<match_id>\w+)$', views.feedback, name='feedback'),
    url(r'^feedback_old/$', views.feedback_old, name='feedback_old'),
    url(r'^feedback_employeerole/$', views.feedback_employeerole, name='feedback_employeerole'),
    url(r'^run/(?P<match_id>\w+)$', views.run, name="run"),
    url(r'^delete/(?P<match_id>\w+)$', views.delete, name="delete"),

    url(r'^a/get_data_table_columns/$', views_ajax.get_data_table_columns, name='get_data_table_columns'),
    url(r'^a/get_data_column/$', views_ajax.get_data_column, name='get_data_column')
]