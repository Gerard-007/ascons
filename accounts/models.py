import cloudinary
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from ascons.utils import unique_slug_generator


def upload_dir(instance, filename):
    return f"{instance.username}/{filename}"


class UserManager(BaseUserManager):

    def create_user(self, email, username, phone, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError('User must provide username')
        if not phone:
            raise ValueError('User must provide valid phone address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username,
            phone,
            password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICE = (("Male", "Male"), ("Female", "Female"))

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True, )
    phone = models.CharField(max_length=14, unique=True)
    avatar = CloudinaryField(
        folder='UsersImages',
        blank=True,
        null=True,
        help_text="You profile image",
        transformation={"quality": "auto:eco"},
        resource_type="image",
    )
    bio = models.TextField(help_text="Tell us more about your achievements", blank=True, null=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, blank=True, null=True)
    birth_day = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_lecturer = models.BooleanField(default=False)
    is_school_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return f"{self.email}"

    def image_url(self):
        if self.avatar:
            return f"{self.avatar.url}"
        return "https://res.cloudinary.com/dptrfsirm/image/upload/v1658665761/bg_logos/logo_ldshh7.png"

    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return f"{self.username}"

    @property
    def name(self):
        return self.username


@receiver(pre_save, sender=User)
def user_pre_save_signal(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_delete, sender=User)
def user_image_delete(sender, instance, **kwargs):
    if instance.avatar:
        cloudinary.uploader.destroy(instance.avatar.public_id)
