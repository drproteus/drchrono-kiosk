from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/$', views.search, name='search'),
    url(r'^checkin/(\d+)/$', views.checkin, name='checkin'),
    url(r'^verify/(\d+)/$', views.verify, name='verify'),
]
