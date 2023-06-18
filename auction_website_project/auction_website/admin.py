from django.contrib import admin
from . models import *

# Register your models here.


admin.site.register(Category, CategoryAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ItemPhoto, AdminItemPhoto)
