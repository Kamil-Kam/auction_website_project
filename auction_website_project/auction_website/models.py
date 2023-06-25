from django.db import models
from . import validators
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from . functions import get_avatars_path
from django.contrib import admin

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.category


class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class Condition(models.Model):
    condition = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.condition


class ConditionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class CustomUser(AbstractUser):
    country = models.CharField(max_length=20, validators=[validators.validate_name])
    city = models.CharField(max_length=30, validators=[validators.validate_name])
    street = models.CharField(max_length=30, validators=[validators.validate_name])
    postcode = models.CharField(max_length=10, validators=[validators.validate_postcode])
    avatar = ResizedImageField(size=[256, 256], upload_to=get_avatars_path,  blank=True, null=True)


class CustomUserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class Item(models.Model):
    description = models.TextField(max_length=2500)
    title = models.CharField(max_length=120)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=240)
    amount = models.IntegerField(default=1)
    user_seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    images = models.ManyToManyField('ItemPhoto', blank=True)
    created_data = models.TimeField(auto_now_add=True, blank=True, null=True)
    main_image = ResizedImageField(size=[1024, 1024], blank=True, null=True)

    def __str__(self):
        return self.title


class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class ItemPhoto(models.Model):
    image = ResizedImageField(size=[1024, 1024])

    def __str__(self):
        return str(self.image)


class AdminItemPhoto(admin.ModelAdmin):
    readonly_fields = ('id',)


"""
built in User model:
username: The username used for authentication. It should be unique.
password: The hashed password for the user.
email: The user's email address. It can be optional or required, depending on your configuration.
first_name: The user's first name.
last_name: The user's last name.
is_active: A boolean flag indicating whether the user account is active or not. Inactive users typically cannot log in.
is_staff: A boolean flag indicating whether the user has staff/administrative access to the Django admin interface.
is_superuser: A boolean flag indicating whether the user has superuser/administrator privileges.
last_login: The timestamp representing the user's last login time.
date_joined: The timestamp representing the user's registration or creation time.
"""
