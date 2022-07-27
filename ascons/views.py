import datetime
from django.shortcuts import render
from django.views import View
from blogs.models import Blog
from courses.models import Course
from events.models import Event
from lecturers.models import Lecturer
from students.models import Student


class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        featured_courses = Course.objects.filter(featured=True).order_by("-created")[:4]
        latest_news = Blog.objects.all().order_by("-created")[:6]
        now = datetime.datetime.now()
        upcoming_events = Event.objects.filter(end_date__gte=now).order_by('-end_date')[:6]
        students_count = Student.objects.all().count()
        teachers_count = Lecturer.objects.all().count()
        context = {
            "featured_courses": featured_courses,
            "latest_news": latest_news,
            "upcoming_events": upcoming_events,
            "students_count": students_count,
            "teachers_count": teachers_count,
        }
        return render(request, self.template_name, context)


class AboutView(View):
    template_name = 'about.html'

    def get(self, request):
        professors = Lecturer.objects.all()
        context = {
            "professors": professors
        }
        return render(request, self.template_name, context)
