# Generated by Django 3.2.14 on 2022-09-13 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, help_text='eg: Dr, Prof etc...', max_length=200, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('degree', models.CharField(blank=True, help_text='Highest qualification eg: Phd, Bsc, Msc etc...', max_length=200, null=True)),
                ('joining_date', models.DateField()),
                ('twitter', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('department', models.ManyToManyField(blank=True, help_text='Courses offered by this department...', to='department.Department')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
