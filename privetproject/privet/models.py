from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class UserInfo(models.Model):
    male = 'male'
    female = 'female'
    sex_choices = [
        (male, 'male'),
        (female, 'female'),
    ]

    full_name = models.CharField(max_length=255)
    sex = models.CharField(max_length=255, choices=sex_choices)
    birth_date = models.DateField()
    native_language = models.CharField(max_length=255)
    other_languages_and_levels = models.CharField(max_length=255)
    contacts = models.ForeignKey('Contacts', on_delete=models.PROTECT, null=True)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, university, **extra_fields):
        if not email:
            raise ValueError("The email is not given")
        user = self.model(
            email=self.normalize_email(email),
            university=university,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, university, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff = True")

        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser = True")
        return self.create_user(email, password, university, **extra_fields)

class User(AbstractBaseUser):
    university = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_buddy = models.BooleanField(default=False)
    user_info = models.ForeignKey(UserInfo, on_delete=models.PROTECT, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['university']

    def __str__(self):
        return self.email

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True


class Contacts(models.Model):
    vk = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    telegram = models.CharField(max_length=255, blank=True)
    whatsapp = models.CharField(max_length=255, blank=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    citizenship = models.CharField(max_length=255)



class Buddy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    buddy_status = models.CharField(max_length=255)