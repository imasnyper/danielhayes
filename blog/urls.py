from django.conf.urls import include, url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<slug>[a-zA-Z0-9\-\_]+)/$', views.DetailView.as_view(), name='detail'),
]
