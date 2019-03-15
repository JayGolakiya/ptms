
from django.urls import path
from newptmsapp.views import *
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^login/$', login),
url(r'^newconductor/$', newconductor),
url(r'^newbus/$', newbus),
url(r'^home/$', home),
url(r'^fare/$', fare),
url(r'^searchbus/$', searchbus),
url(r'^logout/$', logout),
url(r'^auth/$', authentication),  
url(r'^add_conductor/$', add_conductor),
url(r'^add_bus/$', add_bus),
url(r'^addroute/$', addroute),
url(r'^routeadded/$', routeadded),
url(r'^face_detection/$', face_detection),
url(r'^detect_face/$', detect_face),
url(r'^UpdateFareStatus/$', UpdateFareStatus),


]
