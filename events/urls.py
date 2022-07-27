from django.urls import path
from events import views


urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('detail/<slug:slug>', views.EventDetailView.as_view(), name='event_detail'),
]