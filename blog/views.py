import datetime
from dateutil.relativedelta import relativedelta

import pytz
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Post, Tag


def archive():
    """
    makes an annotated list if the months where posts exist,
    and the post count for each month
    :return: post-count-annotated list of months with posts
    """
    # only retrieve posts that have been published
    a = Post.objects.filter(pub_date__lte=timezone.now())

    # add 'month' to context variable which is all the post
    # datetimes truncated to the month
    a = a.annotate(month=TruncMonth('pub_date'))

    # add 'c' to context variable which counts the number of
    # posts in a month
    a = a.values('month').annotate(c=Count('id'))

    # order archive months by the month
    a = a.order_by('month')

    return a
    
def get_published_tags():
    published_tags = []
    published_posts = Post.objects.filter(pub_date__lte=timezone.now())
    for post in published_posts:
        for tag in post.tags.all():
            published_tags.append((tag, tag.frequency()))
       
    # remove duplicate tags from list
    published_tags = list(set(published_tags))
    
    # nice one-liner for sorting the list by the related_post_count, which
    # is the second item in the published_tags tuple. key=lambda x: x[1]
    # tells sort to do this. it then makes a new list of just the first
    # element (the tag object) of the tuple in descending order.
    published_tags = [x for x in sorted(
        published_tags, key=lambda x: x[1], reverse=True)]
    
    return published_tags

class IndexView(ListView):
    template_name = "blog/blog_index.html"
    context_object_name = 'posts'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['archive'] = archive()
        if 'tag' in self.kwargs.keys():
            context['tag'] = Tag.objects.get(tag=self.kwargs['tag'])
            
        context['tags'] = sorted([x[0] for x in get_published_tags()], 
            key=lambda x: x.tag)
            
        return context
        
        
    def get_queryset(self, **kwargs):
        self.queryset = []
        
        if 'tag' in self.kwargs.keys():
            tag_object = Tag.objects.get(tag=self.kwargs['tag'])
            self.queryset = tag_object.post_set.all().filter(
                pub_date__lte=timezone.now())
            self.queryset = self.queryset.order_by('pub_date')
        else:
            self.queryset = Post.objects.filter(pub_date__lte=timezone.now())
            self.queryset = self.queryset.order_by('-pub_date')
            
        return self.queryset


class ArchiveView(ListView):
    # model = Post
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

    # adds extra context to the context variable created by ListView. In this
    # case the month_name and year variables.
    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
    
        context['archive'] = archive()
        context['tags'] = sorted([x[0] for x in get_published_tags()], 
            key=lambda x: x.tag)
        if 'month' in self.kwargs.keys():
            context.update(
                year=self.kwargs['year'], month=self.kwargs['month'])
            context['month_name'] = self.num_month_to_word_month(
                self.kwargs['month'])
        elif 'year' in self.kwargs.keys():
            context.update(year=self.kwargs['year'])

        return context

    # limit queryset to what is in the url.
    # i.e. if only the year is in the url, retrieve all posts
    # from that year. if a month is specified as well, only posts
    # from that month will be added.
    def get_queryset(self, **kwargs):
        utc = pytz.utc
        year_int = int(self.kwargs['year'])
        year = datetime.datetime(year_int, 1, 1, 0, 0, tzinfo=utc)
        queryset = []

        if 'month' in self.kwargs:
            month = int(self.kwargs['month'])
            date1 = datetime.datetime(year_int, month, 1, 0, 0, tzinfo=utc)
            date2 = date1 + relativedelta(months=1)
            queryset = Post.objects.filter(
                pub_date__range=(date1, date2)).order_by('pub_date')
        elif 'year' in self.kwargs:
            next_year = year + relativedelta(years=1)
            queryset = Post.objects.filter(
                pub_date__range=(year, next_year)).order_by('pub_date')

        return queryset


class PostDetailView(DetailView):
    model = Post

    def find_adjacent_posts(self, post):
        """
        Given a post object return the most recent(if exists)
        and the next published(if exists) post.
        :param post: a post object
        :return: previous post, and next post if either exists.
        """
        all_posts = Post.objects.filter(
            pub_date__lte=timezone.now()).order_by('pub_date')
        prev, next = None, None

        for p in all_posts:
            if p.pub_date < post.pub_date:
                prev = p
            if p.pub_date > post.pub_date:
                next = p
                break

        return prev, next

    def get_context_data(self, **kwargs):
        context = super(
            PostDetailView, self).get_context_data(**kwargs)

        context['prev'], \
            context['next'] = self.find_adjacent_posts(
                context['post'])

        context['archive'] = archive()
        context['tags'] = sorted([x[0] for x in get_published_tags()], 
            key=lambda x: x.tag)

        return context


class BlogTagView(ListView):   
    template_name = "blog/blog_tags.html"
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super(BlogTagView, self).get_context_data(**kwargs)
        context['archive'] = archive()
            
        return context
        
    def get_queryset(self, **kwargs):
        return sorted([x[0] for x in get_published_tags()], 
            key=lambda x: x.tag)
            
            
        
