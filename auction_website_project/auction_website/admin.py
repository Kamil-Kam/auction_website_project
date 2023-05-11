from django.contrib import admin
from . models import Category, Account, Stan, Item

# Register your models here.


admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Stan)
admin.site.register(Item)
