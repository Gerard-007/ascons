import cloudinary
from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from ascons.utils import unique_slug_generator


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Blog(models.Model):
    class BlogObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    STATUS = (
        ('draft', 'draft'),
        ('published', 'published'),
    )

    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
    author = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=200)
    image = CloudinaryField(
        folder='NewsImages',
        blank=True,
        null=True,
        help_text="You profile image",
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    slug = models.SlugField(max_length=220, unique_for_date='created')
    description = models.TextField()
    body = models.TextField()
    views = models.PositiveIntegerField(default=0)  # <- here
    created = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=200, choices=STATUS, default='published')
    objects = models.Manager()  # default manager
    blogobjects = BlogObjects()  # custom manager

    class Meta:
        verbose_name_plural = "Blogs"
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"{self.title} by {self.author.username}"

    @property
    def name(self):
        return f"{self.title}-{self.created}"

    def image_url(self):
        if self.image:
            return f"{self.image.url}"
        return "https://res.cloudinary.com/dptrfsirm/image/upload/v1658601579/bg_logos/logo_dygcg3.png"


@receiver(pre_save, sender=Blog)
def blog_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_delete, sender=Blog)
def blog_image_delete(sender, instance, **kwargs):
    if instance.image:
        cloudinary.uploader.destroy(instance.image.public_id)
