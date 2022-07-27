from django.db import models
from accounts.models import User
from courses.models import Course


class Department(models.Model):
    dept_name = models.CharField(max_length=200)
    dept_head = models.ForeignKey(User, on_delete=models.CASCADE)
    dept_courses = models.ManyToManyField(Course, blank=True)
    starting_year = models.DateField()
    student_capacity = models.IntegerField(default=0)
    # dept_name, hod, phone, email, starting_year, student_capacity

    def __str__(self):
        return f"{self.dept_name}"
