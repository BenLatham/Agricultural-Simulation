from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$|^index$', views.index, name='index'),
    url(r'^process/([0-9]+)$', views.run_process, name='run'),
    url(r'^report/([0-9]+)$', views.report, name='report')
]

