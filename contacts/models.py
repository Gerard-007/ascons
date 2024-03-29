from email import message
from django.db import models
from datetime import datetime


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    contact_date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self) -> str:
        return self.email
