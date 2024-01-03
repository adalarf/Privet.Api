from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import secrets
from django.core.mail import send_mail



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
    other_languages_and_levels = models.CharField(max_length=255, blank=True)
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
    is_teamlead = models.BooleanField(default=False)
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


class ArrivalBooking(models.Model):
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    flight_number = models.CharField(max_length=255)
    arrival_point = models.CharField(max_length=255)
    comment = models.CharField(max_length=255, blank=True)
    other_students = models.ManyToManyField('Student', related_name='other_students', blank=True)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    citizenship = models.CharField(max_length=255)
    arrival_booking = models.OneToOneField(ArrivalBooking, on_delete=models.PROTECT, null=True)
    only_view = models.OneToOneField('StudentOnlyViewFields', on_delete=models.PROTECT, null=True)
    confirmation_code = models.CharField(max_length=6, null=True, blank=True)

    def send_confirmation_email(self):
        code = secrets.token_hex(3)  # Генерация случайного кода из 6 символов
        self.confirmation_code = code
        self.save()
        subject = 'Подтверждение регистрации'
        message = f'Ваш код подтверждения: {code}'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.user.email])

    def confirm_registration(self, entered_code):
        if self.confirmation_code == entered_code:
            self.confirmation_code = None
            self.user.is_active = True
            self.user.save()
            self.save()
            return True
        return False


class StudentOnlyViewFields(models.Model):
    institute = models.CharField(max_length=255, blank=True, null=True)
    study_program = models.CharField(max_length=255, blank=True, null=True)
    last_visa_expiration = models.DateField(blank=True, null=True)
    accommodation = models.CharField(max_length=255, blank=True, null=True)
    buddys_comment = models.CharField(max_length=255, blank=True, null=True)


class BuddyArrival(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)


class Buddy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    buddy_status = models.CharField(max_length=255)
    buddy_arrivals = models.ManyToManyField(BuddyArrival, related_name='buddy')
    is_confirmed = models.BooleanField(default=False)