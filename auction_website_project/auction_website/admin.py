from django.contrib import admin
from . models import Category, Account, Condition, Item, CustomUser

# Register your models here.


admin.site.register(Category)
admin.site.register(Account)
admin.site.register(Condition)
admin.site.register(Item)
admin.site.register(CustomUser)