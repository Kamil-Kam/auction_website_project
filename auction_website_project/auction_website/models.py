from django.db import models
from . import validators
from django.core.exceptions import ValidationError

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.category


class Condition(models.Model):
    condition = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.condition


class Account(models.Model):
    email = models.EmailField(unique=True, validators=[validators.validate_email])
    username = models.CharField(max_length=20, unique=True, validators=[validators.validate_username])
    firstname = models.CharField(max_length=20, validators=[validators.validate_name])
    surname = models.CharField(max_length=20, validators=[validators.validate_name])
    country = models.CharField(max_length=20, validators=[validators.validate_name])
    city = models.CharField(max_length=30, validators=[validators.validate_name])
    street = models.CharField(max_length=30, validators=[validators.validate_name])
    postcode = models.CharField(max_length=10, validators=[validators.validate_postcode])
    password = models.CharField(max_length=100)
    avatar = models.ImageField(blank=True, null=True)

    def __str__(self):
        return '%s %s %s' % (self.username, self.firstname, self.surname)


class Item(models.Model):
    description = models.TextField(max_length=2500)
    title = models.CharField(max_length=120)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=240)
    amount = models.IntegerField(default=1)
    # user = models.ForeignKey(Account, on_delete=models.CASCADE)
    # images = models.ManyToManyField('ItemPhoto')

    def __str__(self):
        return self.title


class ItemPhoto(models.Model):
    image = models.ImageField()




