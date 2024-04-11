import random
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.core import validators


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username,
                          email=email,
                          is_staff=is_staff,
                          is_active=is_staff, is_superuser=is_superuser, date_joined=now, **extra_fields)
        if not extra_fields.get('no_password'):
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

        return self._create_user(username, phone_number, email, password, False, False, **extra_fields)

    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})

# class UserManager(BaseUserManager):
#     def create_user(self, phone, password=None):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not phone:
#             raise ValueError("Users must have an phone number")
#
#         user = self.model(
#             phone=phone
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

    # def create_superuser(self, phone, password=None):
    #     """
    #     Creates and saves a superuser with the given email, date of
    #     birth and password.
    #     """
    #     user = self.create_user(
    #         phone,
    #         password=password,
    #     )
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, unique=True, validators=[
        validators.RegexValidator(r'^[a-zA-Z][a-zA-Z0-9_\.]+$', 'Enter a valid username')
    ], error_messages={'unique': 'A user with that username already'})

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True,
                                    # validators=[
                                    #     validators.RegexVlidator(r'^989[0-3,9]\d{8}$', 'Enter a valid')
                                    # ]
                                    )
    is_staff = models.BooleanField(default=False, help_text='Designates whether the user can log into this admin')
    is_active = models.BooleanField(default=True, help_text='Designates whether this user should be treated as active')
    date_joined = models.DateTimeField(default=timezone.now, blank=True)
    last_seen = models.DateTimeField(null=True)

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'users'
        verbose_name = 'users'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='profile', blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.BooleanField(help_text='female is False, male is True, null is unset', null=True, blank=True)
    province = models.ForeignKey(to='Province', null=True, on_delete=models.SET_NULL)

    # email = models.EmailField(max_length=254, unique=True)
    # phone_number = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    @property
    def get_first_name(self):
        return self.user.first_name

    @property
    def get_last_name(self):
        return self.user.last_name

    def get_nick_name(self):
        return self.nick_name if self.nick_name else self.user.username


class Divice(models.Model):
    WEB = 1
    IOS = 2
    ANDROID = 3
    DEVICE_TYPE_CHOICES = (
        (WEB, 'web'),
        (IOS, 'ios'),
        (ANDROID, 'android')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device')
    device_uuid = models.UUIDField(null=True)
    last_login = models.DateTimeField(null=True)
    device_type = models.PositiveSmallIntegerField(choices=DEVICE_TYPE_CHOICES, default=ANDROID)
    device_os = models.CharField(max_length=20, blank=True)
    device_model = models.CharField(max_length=50, blank=True)
    app_version = models.CharField(max_length=20, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # db_table = 'user-device'
        verbose_name = 'device'
        verbose_name_plural = 'devices'
        unique_together = ('user', 'device_uuid')


class Province(models.Model):
    name = models.CharField(max_length=50)
    is_valid = models.BooleanField(default=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
