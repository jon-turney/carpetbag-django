from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^raw/(.*)', views.rawlog, name='raw'),
    url(r'^log/(.*)', views.log,    name='log'),
    url(r'^$',        views.index,  name='index'),
]

