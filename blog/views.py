from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime
import pytz

from django.db.models.functions import TruncMonth
from django.db.models import Count

# Create your views here.
from .models import Post


class IndexView(ListView):
    template_name = "blog/blog_index.html"
    queryset = Post.objects.filter(pub_date__lte=timezone.now())
    queryset = queryset.order_by('-pub_date')
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['archive'] = Post.objects.filter(pub_date__lte=timezone.now()).annotate(month=TruncMonth('pub_date')).values('month').annotate(c=Count('id'))

        return context


class ArchiveView(ListView):
    template_name = "blog/blog_archive.html"
    # queryset = Post.objects.filter(pub_date__lte=timezone.now())
    # queryset = queryset.order_by('-pub_date')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        print(kwargs)
        context['posts'] = Post.objects.filter(pub_date__month=self.kwargs['month'])
        context['posts'] = context['posts'].filter(pub_date__lte=timezone.now())
        context['posts'] = context['posts'].order_by('-pub_date')
        
        context['archive'] = Post.objects.filter(pub_date__lte=timezone.now())
        context['archive'] = context['archive'].annotate(month=TruncMonth('pub_date'))
        context['archive'] = context['archive'].values('month').annotate(c=Count('id'))
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
