from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .utils import RoleEnum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, name, surname, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")
        if not name:
            raise ValueError("Users must have a name")
        if not surname:
            raise ValueError("Users must have a surname")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            surname=surname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, surname, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            name=name,
            surname=surname,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=RoleEnum.choices(), default=RoleEnum.REGISTERED_USER)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'surname']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Destination(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=50)
    state = models.CharField(max_length=200, null=True)
    longitude = models.DecimalField(max_digits=50, decimal_places=38)
    latitude = models.DecimalField(max_digits=50, decimal_places=38)

    def __str__(self):
        return self.name + ', ' + self.country


class Parcel(models.Model):
    destination_from = models.ForeignKey(Destination, null=False, on_delete=models.CASCADE,
                                         related_name='destination_from')
    destination_to = models.ForeignKey(Destination, null=False, on_delete=models.CASCADE, related_name='destination_to')
    weight = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    price = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    sender = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='receiver')


class Train(models.Model):
    start_destination = models.ForeignKey(Destination, null=True, on_delete=models.SET_NULL,
                                          related_name='start_destination')

#
# class Route(models.Model):
#     train = models.ForeignKey(Train, null=False, on_delete=models.CASCADE, related_name='train')
#     destinations = models.ManyToManyField(Destination)
