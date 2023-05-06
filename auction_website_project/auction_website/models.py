from django.db import models

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
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    stan = models.ForeignKey(Stan, on_delete=models.SET_NULL)
    location = models.CharField(max_length=240)

    def __str__(self):
        return self.title


