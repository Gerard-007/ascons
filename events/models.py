import cloudinary
from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from ascons.utils import unique_slug_generator


class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique_for_date='created')
    description = models.TextField()
    image = CloudinaryField(
        folder='EventsImages',
        blank=True,
        null=True,
        help_text="School event images",
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    address = models.CharField(max_length=225)
    speakers = models.ManyToManyField("accounts.User", blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # still_ongoing = models.BooleanField(default=True)
    created = models.DateTimeField(auto_created=True)
    featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Events"
        ordering = ("-created",)

    def __str__(self) -> str:
        return self.name

    def image_url(self):
        if self.image:
            return f"{self.image.url}"
        return "https://res.cloudinary.com/dptrfsirm/image/upload/v1658601579/bg_logos/logo_dygcg3.png"


@receiver(pre_save, sender=Event)
def event_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_delete, sender=Event)
def event_image_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)
