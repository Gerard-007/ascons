from django.urls import path
from blogs.api import views

urlpatterns = [
    path('<int:pk>/', views.BlogDetail.as_view(), name='blog_detail_api'),
    path('', views.BlogList.as_view(), name='blog_list_api'),
    # path('create/', views.plan_create, name='plan_create_api'),
    # path('update/<slug:slug>/', views.plan_update, name='plan_update_api'),
    # path('delete/<slug:slug>/', views.plan_delete, name='plan_delete_api'),
]