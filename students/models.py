from django.db import models
from accounts.models import User
from department.models import Department


class Student(models.Model):
    roll_no = models.CharField(max_length=100)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    admission_date = models.DateField()
    # image, roll-no, name, department, mobile, email, admission date

    def __str__(self):
        return f"{self.name.get_full_name}"
