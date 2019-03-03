from django.urls import path, register_converter

from . import views, converters

register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoDigitMonthConverter, 'mm')

app_name = 'blog'

urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("tags/", views.BlogTagView.as_view(), name='tags-index'),
    path("tags/<slug:tag>/", views.IndexView.as_view(), name="tags"),
    path("archive/<yyyy:year>/<mm:month>/", views.ArchiveView.as_view(), name='archive'),
    path("archive/<yyyy:year>/", views.ArchiveView.as_view(), name='archive'),
    path("contact/", views.contact, name='contact'),
    path("<slug:slug>/", views.PostDetailView.as_view(), name='detail'),
]

# urlpatterns = [
#     url(r'^$', views.IndexView.as_view(), name='home'),
#     url(r'^tags/(?P<tag>[a-zA-Z0-9\-\_ ]+)/$',
#         views.IndexView.as_view(), name='tags'),
#     url(r'^tags/$', views.BlogTagView.as_view(), name='tags'),
#     url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', views.ArchiveView.as_view(), name='archive'),
#     url(r'^(?P<year>\d{4})/$', views.ArchiveView.as_view(), name='archive'),
#     url(r'^(?P<slug>[a-zA-Z0-9\-\_]+)/$',
#         views.PostDetailView.as_view(), name='detail'),
#     path('contact/', views.contact, name='contact'),
# ]
