from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^summary/$', views.summary, name='summary'),
    url(r'^view/(?P<alpha_or_beta>\w+)$', views.view, name="view_dataset"),
]