from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^auto/$', views.sign_in, name="sign_in"),
    url(r'^auto/profile/$', views.get_profile, name="profile"),
    url(r'^auto/sign_out/$', views.sign_out, name="sign_out"),
    url(r'^auto/submit/$', views.submit, name="submit"),
    url(r'^auto/postFeedback/$', views.postReview, name="postReview"),
    url(r'^auto/deleteReviews/$', views.deleteReviews, name="deleteReviews"),
]
