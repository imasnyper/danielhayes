from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Create your views here.
from .models import Post


class IndexView(ListView):
    template_name = "blog/blog_index.html"
    queryset = Post.objects.all().order_by('-pub_date')
    context_object_name = 'latest_posts'
    paginate_by = 5



# class IndexView(TemplateView):
#     template_name = "blog/blog_index.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(IndexView, self).get_context_data(**kwargs)
#         context['latest_posts'] = Post.objects.all().order_by('-pub_date')[:5]
#
#         return context


class DetailView(DetailView):
    model = Post
