from django.contrib import admin
from . import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'start_date', 'created', 'featured',)
    list_filter = ['featured']
    prepopulated_fields = {"slug": ('name',)}
