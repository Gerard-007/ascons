from django.contrib import admin
from . import models

@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'featured',)
    prepopulated_fields = {"slug": ('name',)}
