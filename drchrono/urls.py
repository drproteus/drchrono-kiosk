from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^enable_kiosk/$', views.enable_kiosk, name='enable_kiosk'),
    url(r'^disable_kiosk/$', views.disable_kiosk, name='disable_kiosk'),
    url(r'^config/$', views.config, name='config'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^kiosk/', include('kiosk.urls', namespace='kiosk')),
]
