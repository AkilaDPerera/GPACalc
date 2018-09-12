from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^auto/$', views.sign_in, name="sign_in"),
    url(r'^auto/profile/$', views.get_profile, name="profile"),
    url(r'^auto/userProfile/$', views.load_home_profile_page, name="load_home_profile_page"),
    url(r'^auto/sign_out/$', views.sign_out, name="sign_out"),
    url(r'^auto/submit/$', views.submit, name="submit"),
    url(r'^auto/postFeedback/$', views.postReview, name="postReview"),
    url(r'^auto/deleteReviews/$', views.deleteReviews, name="deleteReviews"),
    url(r'^auto/getMarkSheetURLs/$', views.getMarkSheetURLs, name="getMarkSheetURLs"),
    url(r'^auto/submitURL/$', views.submitURL, name="submitURL"),
    url(r'^auto/cancelURL/$', views.cancelURL, name="cancelURL"),
    url(r'^reports/$', views.reports, name="reports"),
    url(r'^reports/getReportData/$', views.getReportData, name="reportData"),
    url(r'^reports/(?P<index>[0-9]{6}[a-zA-Z]{1})/$', views.getReportProfile, name="reportProfile")
]
