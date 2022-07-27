from django.db import models
from accounts.models import User


class Lecturer(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, help_text="eg: Dr, Prof etc...", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    department = models.ManyToManyField("department.Department", help_text="Courses offered by this department...", blank=True)
    degree = models.CharField(max_length=200, help_text="Highest qualification eg: Phd, Bsc, Msc etc...", blank=True, null=True)
    joining_date = models.DateField()
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    # image, name, department, gender, degree, mobile, email, address, joining date

    def __str__(self):
        return f"{self.name.get_full_name}"
