from django.contrib import admin
from . import models


@admin.register(models.Blog)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'slug', 'author',)
    list_filter = ['author', 'status']
    prepopulated_fields = {"slug": ('title',), }


admin.site.register(models.Category)
