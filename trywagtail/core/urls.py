from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^images/(\d+)/use/$', views.use_image, name='use_image')
]
