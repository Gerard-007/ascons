from rest_framework import generics
from blogs.models import Blog
from .serializers import BlogSerializer


class BlogList(generics.ListCreateAPIView):
    queryset = Blog.blogobjects.all()
    serializer_class = BlogSerializer


class BlogDetail(generics.RetrieveDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
