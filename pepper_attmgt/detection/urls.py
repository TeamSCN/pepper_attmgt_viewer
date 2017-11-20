from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.detect_received_image, name='detection'),
]
