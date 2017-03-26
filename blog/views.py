from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils import timezone

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
        if 'year' in self.kwargs.keys() and 'month' in self.kwargs.keys():
            context.update(year=self.kwargs['year'], month=self.kwargs['month'])
        elif 'year' in self.kwargs.keys():
            context.update(year=self.kwargs['year'])

        return context

    def get_queryset(self):
        if 'month' in self.kwargs:
            month = str(self.kwargs['month'])
            next_month = str(int(month) + 1)
            year = str(self.kwargs['year'])
            queryset = Post.objects.filter(pub_date__range=("%s-%s-01 00:00" % (year, month), "%s-%s-01 00:00" % (year, next_month))).order_by('pub_date')

        elif 'year' in self.kwargs:
            year = str(self.kwargs['year'])
            next_year = str(int(year) + 1)
            queryset = Post.objects.filter(pub_date__range=("%s-01-01 00:00" % year, "%s-01-01 00:00" % next_year)).order_by('pub_date')
        return queryset


class DetailView(DetailView):
    model = Post
