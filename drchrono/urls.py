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
    url(r'^see_patient/(\d+)/$', views.see_patient, name='see_patient'),
    url(r'^complete_appointment/(\d+)/$', views.complete_appointment,
        name='complete_appointment'),
    url(r'^archive/$', views.archive, name="archive"),
    url(r'^reset/(\d+)/$', views.reset_to_arrived, name="reset"),
    url(r'^wait_time/$', views.get_time_info, name="wait_time"),
    url(r'^arrivals/$', views.get_arrivals, name="arrivals"),
    url(r'^check_if_new/$', views.check_if_new_arrivals),
    url(r'^get_notes/(\d+)/$', views.get_notes_form, name="get_notes"),
    url(r'^update_notes/(\d+)/$', views.update_notes, name="update_notes"),
    url(r'^kiosk/', include('kiosk.urls', namespace='kiosk')),
]
