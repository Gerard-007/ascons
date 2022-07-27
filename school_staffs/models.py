from django.db import models
from accounts.models import User


class SchoolStaff(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    joining_date = models.DateField()
    # image, name, designation, mobile, email, address, joining date

    def __str__(self):
        return f"{self.name.get_full_name}"
