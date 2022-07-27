from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from blogs.models import Blog


class BlogListView(ListView):
    model = Blog
    context_object_name = "blogs"
    template_name = "blogs/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['latest_blog'] = Blog.objects.all().first()
        return context


class BlogDetailView(DetailView):
    model = Blog
    context_object_name = "blog"
    template_name = "blogs/details.html"

    def get_object(self, **kwargs):
        view_count_obj = super(BlogDetailView, self).get_object()
        view_count_obj.views += 1
        view_count_obj.save()
        return view_count_obj
