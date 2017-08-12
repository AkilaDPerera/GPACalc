from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
	url(r'^personal/$', views.personal, name='personal'),
	url(r'^professional/$', views.professional, name='professional'),
	url(r'^projects/$', views.projects, name='projects'),
	url(r'^contact/$', views.contact, name='contact'),
    url(r'^get_user/$', views.getUser, name='getUser'),
]
