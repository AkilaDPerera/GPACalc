from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.professional, name='home'),
	url(r'^professional/$', views.professional, name='professional'),
    url(r'^get_user/$', views.getUser, name='getUser'),
]
