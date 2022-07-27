from django.urls import path
from courses import views


urlpatterns = [
    path('', views.CourseListView.as_view(), name='course_list'),
    path('detail/<slug:slug>', views.CourseDetailView.as_view(), name='course_detail'),
]
