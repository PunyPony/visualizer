from . import views
from django.conf.urls import url
from django.urls import path, re_path


urlpatterns = [
    url(r'', views.home, name='home'),
    url(r'^slice_(?P<axis>[XYZ])/(?P<slice_nb>\d+)/(?P<file_name>[\w.]+)$', views.getSlice, name='getSlice'),
    url(r'^histogram/(?P<file_name>[\w.]+)$', views.getHist, name='getHist'),
    url(r'^histogram/(?P<file_name>[\w.]+)/(?P<mask_name>[\w.]+)$', views.getMaskHist, name='getMaskHist'),
]