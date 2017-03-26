from django.conf.urls import include, url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', views.ArchiveView.as_view(), name='archive'),
    url(r'^(?P<year>\d{4})/$', views.ArchiveView.as_view(), name='archive'),
    url(r'^(?P<slug>[a-zA-Z0-9\-\_]+)/$', views.DetailView.as_view(), name='detail'),
]
