import cloudinary
from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from ascons.utils import unique_slug_generator


class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique_for_date='created', blank=True, null=True)
    instructor = models.ManyToManyField("lecturers.Lecturer", related_name="lecturer", blank=True)
    students = models.ManyToManyField("students.Student", related_name="student", blank=True)
    image = CloudinaryField(
        folder='CoursesImages',
        blank=True,
        null=True,
        help_text="School course images",
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    description = models.TextField()
    start_date = models.DateTimeField()
    created = models.DateTimeField(auto_created=True)
    featured = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Courses"
        ordering = ("-created",)

    def image_url(self):
        if self.image:
            return f"{self.image.url}"
        return "https://res.cloudinary.com/dptrfsirm/image/upload/v1658736143/bg_logos/1636087167843_ridyji.jpg"

    @property
    def get_num_of_enrolled_students(self):
        return self.students.all().count()


@receiver(pre_save, sender=Course)
def course_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_delete, sender=Course)
def course_image_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)
