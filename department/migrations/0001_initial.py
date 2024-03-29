# Generated by Django 3.2.14 on 2022-09-13 14:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=200)),
                ('starting_year', models.DateField()),
                ('student_capacity', models.IntegerField(default=0)),
                ('dept_courses', models.ManyToManyField(blank=True, to='courses.Course')),
                ('dept_head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
