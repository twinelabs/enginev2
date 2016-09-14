from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create/$', views.create, name='create'),
    url(r'^create_employeerole/$', views.create_employeerole, name='create_employeerole'),
    url(r'^view/(?P<match_id>\w+)$', views.view, name="view"),
    url(r'^analyze/(?P<match_id>\w+)$', views.analyze, name="analyze"),
    url(r'^feedback/(?P<match_id>\w+)$', views.feedback, name='feedback'),
    url(r'^feedback_employeerole/$', views.feedback_employeerole, name='feedback_employeerole'),
    url(r'^run/(?P<match_id>\w+)$', views.run, name="run"),
    url(r'^delete/(?P<match_id>\w+)$', views.delete, name="delete"),
    url(r'^ajax/data_table_columns/$', views.data_table_columns, name='data_table_columns')
]