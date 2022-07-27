from rest_framework import serializers
from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "name",
            "code",
            "description",
            "start_date",
            "featured",
        )
