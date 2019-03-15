from django.contrib import admin
from django.conf.urls import url,include
from django.conf.urls import handler404

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('newptmsapp.urls')),
]
handler404='myapp.views.error_404_view'