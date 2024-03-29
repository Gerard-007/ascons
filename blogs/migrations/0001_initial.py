# Generated by Django 3.2.14 on 2022-09-13 14:16

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', cloudinary.models.CloudinaryField(blank=True, help_text='You profile image', max_length=255, null=True)),
                ('slug', models.SlugField(max_length=220, unique_for_date='created')),
                ('description', models.TextField()),
                ('body', models.TextField()),
                ('views', models.PositiveIntegerField(default=0)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('draft', 'draft'), ('published', 'published')], default='published', max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='blogs.category')),
            ],
            options={
                'verbose_name_plural': 'Blogs',
                'ordering': ('-created',),
            },
        ),
    ]
