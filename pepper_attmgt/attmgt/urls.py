from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
urlpatterns = [
    url(r'^image/$', views.receive_image, name='image'),
]
