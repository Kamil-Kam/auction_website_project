from django.db import models
from . import validators

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.category


class Stan(models.Model):
    stan = models.CharField(max_length=120, null=False, blank=False)

    def __str__(self):
        return self.stan


class Item(models.Model):
    description = models.TextField(max_length=2500)
    title = models.CharField(max_length=120)
    price = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    stan = models.ForeignKey(Stan, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=240)

    def __str__(self):
        return self.title


class Account(models.Model):
    nickname = models.CharField(max_length=20)
    firstname = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    postcode = models.CharField(max_length=10)
    password = models.CharField(max_length=20, validators=[validators.validate_password])

    def __str__(self):
        return '%s %s %s' % (self.nickname, self.firstname, self.surname)

