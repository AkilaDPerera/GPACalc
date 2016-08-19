from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.basic),
    url(r'^signin/$', views.signinPage),
    url(r'^signin/submit/$', views.signin),
    url(r'^signin/submit/choice1/$', views.choice1),
    url(r'^signin/submit/choice2/$', views.choice2),
    url(r'^signin/submit/choice2/choice2_post/$', views.choice2_post),

    url(r'^manual/$', views.manual)
]