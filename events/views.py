from django.views.generic import ListView, DetailView
from events.models import Event


class EventListView(ListView):
    model = Event
    context_object_name = 'events'
    template_name = "events/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['latest_event'] = Event.objects.all().first()
        context['featured_event'] = Event.objects.filter(featured=True).first()
        return context


class EventDetailView(DetailView):
    model = Event
    context_object_name = 'event'
    template_name = "events/details.html"