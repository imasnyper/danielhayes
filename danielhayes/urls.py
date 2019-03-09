"""danielhayes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap, Sitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, reverse
from django.utils import timezone

from blog.models import Post

info_dict = {
    'queryset': Post.objects.filter(pub_date__lte=timezone.now()),
    'date_field': 'pub_date',
}


class StaticViewSitemap(Sitemap):
    priority = 0.75
    changefreq = 'daily'

    def items(self):
        return ['blog:contact']

    def location(self, item):
        return reverse(item)


sitemaps = {
    'static': StaticViewSitemap,
    'blog': GenericSitemap(info_dict, priority=1.0),
}

urlpatterns = [
    # path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
