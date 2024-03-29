from rest_framework import serializers
from events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "name",
            "address",
            "description",
            "start_date",
            "end_date",
            "featured",
        )