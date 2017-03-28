from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime
import pytz

# Create your views here.
from .models import Post


class IndexView(ListView):
    template_name = "blog/blog_index.html"
    queryset = Post.objects.all().order_by('-pub_date')
    context_object_name = 'posts'
    paginate_by = 5


class ArchiveView(ListView):
    template_name = "blog/blog_archive.html"
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        if 'month' in self.kwargs.keys():
            context.update(year=self.kwargs['year'], month=self.kwargs['month'])
        elif 'year' in self.kwargs.keys():
            context.update(year=self.kwargs['year'])

        return context

    def get_queryset(self):
        utc = pytz.utc
        year_int = int(self.kwargs['year'])
        year = datetime.datetime(year_int, 1, 1, 0, 0, tzinfo=utc)

        if 'month' in self.kwargs:
            month = int(self.kwargs['month'])
            date1 = datetime.datetime(year_int, month, 1, 0, 0, tzinfo=utc)
            date2 = date1 + relativedelta(months=1)
            queryset = Post.objects.filter(pub_date__range=(date1, date2)).order_by('pub_date')
        elif 'year' in self.kwargs:
            next_year = year + relativedelta(years=1)
            queryset = Post.objects.filter(pub_date__range=(year, next_year)).order_by('pub_date')
        return queryset


class DetailView(DetailView):
    model = Post
