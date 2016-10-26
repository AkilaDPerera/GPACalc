from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.twoOption),
    url(r'^auto/$', views.auto),
    url(r'^auto/profile/$', views.profile),
    url(r'^auto/profile2/$', views.profile2),
    url(r'^auto/profile/chageGrades/$', views.changeGrades)
]
