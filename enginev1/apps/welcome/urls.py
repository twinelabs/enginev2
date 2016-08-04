from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'client/(?P<pk>[0-9]+)/$', views.ClientUpdate.as_view(), name='client-update'),
    url(r'^home/$', views.home, name='home'),
    url(r'^$', views.home, name='home'),
]