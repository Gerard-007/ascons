from django.urls import path
from events.api import views

urlpatterns = [
    path('<int:pk>/', views.EventDetail.as_view(), name='event_detail_api'),
    path('', views.EventList.as_view(), name='event_list_api'),
    # path('create/', views.plan_create, name='plan_create_api'),
    # path('update/<slug:slug>/', views.plan_update, name='plan_update_api'),
    # path('delete/<slug:slug>/', views.plan_delete, name='plan_delete_api'),
]