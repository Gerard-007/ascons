from django.shortcuts import render
from django.views.generic import ListView, DetailView

from courses.models import Course


class CourseListView(ListView):
    model = Course
    context_object_name = 'courses'
    template_name = "courses/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['latest_course'] = Course.objects.all().first()
        context['featured_course'] = Course.objects.filter(featured=True).first()
        return context


class CourseDetailView(DetailView):
    model = Course
    context_object_name = 'course'
    template_name = "courses/details.html"
