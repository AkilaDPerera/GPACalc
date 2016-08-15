from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.basic),
	url(r'^signin/$', views.signin),
	url(r'^signin/submit/$', views.btn1),
	url(r'^signin/submit/result/$', views.result),
	url(r'^manual/$', views.manual)
]