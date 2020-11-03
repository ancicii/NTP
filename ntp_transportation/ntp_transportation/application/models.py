from django.core.validators import MinValueValidator
from django.db import models
from .utils import RoleEnum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, name, surname, address, mobile, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")
        if not name:
            raise ValueError("User must have a name")
        if not surname:
            raise ValueError("User must have a surname")
        if not address:
            raise ValueError("User must have an address")
        if not mobile:
            raise ValueError("User must have a phone number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            surname=surname,
            address=address,
            mobile=mobile,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, surname, address, mobile, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            name=name,
            surname=surname,
            address=address,
            mobile=mobile,
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
    address = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    mobile = PhoneNumberField(null=False, blank=False, unique=True, max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'surname', 'address', 'mobile']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Parcel(models.Model):
    destination_from = models.CharField(max_length=200)
    destination_to = models.CharField(max_length=200)
    weight = models.FloatField(default=0, validators=[MinValueValidator(0)])
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    sender = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='receiver')
    dateCreated = models.DateTimeField(verbose_name='date created', auto_now_add=True)
    dateSent = models.DateTimeField(verbose_name='date sent', auto_now_add=False, null=True)
    isDelivered = models.BooleanField(default=False)
    isSent = models.BooleanField(default=False)
    isApproved = models.BooleanField(default=True)
    isDeclined = models.BooleanField(default=False)
    senderName = models.CharField(max_length=200, null=True)
    senderSurname = models.CharField(max_length=200, null=True)
    senderContact = PhoneNumberField(null=False, blank=False, unique=False, max_length=200)
    receiverName = models.CharField(max_length=200, null=True)
    receiverSurname = models.CharField(max_length=200, null=True)
    receiverContact = PhoneNumberField(null=False, blank=False, unique=False, max_length=200)
    description = models.CharField(max_length=500)


class Train(models.Model):
    start_destination = models.CharField(max_length=200)
    isAvailable = models.BooleanField(default=True)


class Route(models.Model):
    train = models.ForeignKey(Train, null=False, on_delete=models.CASCADE, related_name='train')
    destinations = models.TextField(null=True)
