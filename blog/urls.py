from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^tags/(?P<tag>[a-zA-Z0-9\-\_ ]+)/$',
        views.IndexView.as_view(), name='tags'),
    url(r'^tags/$', views.BlogTagView.as_view(), name='tags'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', views.ArchiveView.as_view(), name='archive'),
    url(r'^(?P<year>\d{4})/$', views.ArchiveView.as_view(), name='archive'),
    url(r'^(?P<slug>[a-zA-Z0-9\-\_]+)/$',
        views.PostDetailView.as_view(), name='detail'),
]
