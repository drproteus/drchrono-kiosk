from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

import views


urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', views.logout_view),
]
