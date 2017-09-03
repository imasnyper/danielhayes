import datetime
from dateutil.relativedelta import relativedelta

import pytz
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Create your views here.
from .models import Post


class IndexView(ListView):
    template_name = "blog/blog_index.html"
    queryset = Post.objects.filter(pub_date__lte=timezone.now())
    queryset = queryset.order_by('-pub_date')
    context_object_name = 'posts'
    paginate_by = 5

    def archive(self):
        a = Post.objects.filter(pub_date__lte=timezone.now())  # only retrieve posts that have been published

        # add 'month' to context variable which is all the post datetimes truncated to the month
        a = a.annotate(month=TruncMonth('pub_date'))

        # add 'c' to context variable which counts the number of posts in a month
        a = a.values('month').annotate(c=Count('id'))

        # order archive months by the month
        a = a.order_by('month')

        return a

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['archive'] = self.archive()
        # context['archive'] = Post.objects.filter(
        #     pub_date__lte=timezone.now()).annotate(
        #     month=TruncMonth('pub_date')).values(
        #     'month').annotate(
        #     c=Count('id'))
        # context['archive'] = context['archive'].order_by('month')

        return context


class ArchiveView(ListView):
    template_name = "blog/blog_archive.html"
    # queryset = Post.objects.filter(pub_date__lte=timezone.now())
    # queryset = queryset.order_by('-pub_date')
    paginate_by = 5

    def num_month_to_word_month(self, month_num):
        month_name_dict = {1: 'January',
                           2: 'February',
                           3: 'March',
                           4: 'April',
                           5: 'May',
                           6: 'June',
                           7: 'July',
                           8: 'August',
                           9: 'September',
                           10: 'October',
                           11: 'November',
                           12: 'December'}
        month_num = int(month_num)
        return month_name_dict[month_num]

    def archive(self):
        a = Post.objects.filter(pub_date__lte=timezone.now())  # only retrieve posts that have been published

        # add 'month' to context variable which is all the post datetimes truncated to the month
        a = a.annotate(month=TruncMonth('pub_date'))

        # add 'c' to context variable which counts the number of posts in a month
        a = a.values('month').annotate(c=Count('id'))

        # order archive months by the month
        a = a.order_by('month')

        return a

    # adds extra context to the context variable created by ListView. In this case the month_name and year variables.
    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)

        context['archive'] = self.archive()
        if 'month' in self.kwargs.keys():
            context.update(year=self.kwargs['year'], month=self.kwargs['month'])
            context['month_name'] = self.num_month_to_word_month(self.kwargs['month'])
        elif 'year' in self.kwargs.keys():
            context.update(year=self.kwargs['year'])

        return context

    def get_queryset(self, **kwargs):
        utc = pytz.utc
        year_int = int(self.kwargs['year'])
        year = datetime.datetime(year_int, 1, 1, 0, 0, tzinfo=utc)
        queryset = []

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

    def archive(self):
        # only retrieve posts that have been published
        a = Post.objects.filter(pub_date__lte=timezone.now())

        # add 'month' to context variable which is all the post datetimes truncated to the month
        a = a.annotate(month=TruncMonth('pub_date'))

        # add 'c' to context variable which counts the number of posts in a month
        a = a.values('month').annotate(c=Count('id'))

        # order archive months by the month
        a = a.order_by('month')

        return a

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        context['archive'] = self.archive()
        # context['archive'] = Post.objects.filter(
        #     pub_date__lte=timezone.now()).annotate(
        #     month=TruncMonth('pub_date')).values(
        #     'month').annotate(
        #     c=Count('id'))
        # context['archive'] = context['archive'].order_by('month')

        return context
