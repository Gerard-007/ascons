from django.urls import path
from blogs import views


urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('detail/<slug:slug>', views.BlogDetailView.as_view(), name='blog_detail'),
]
