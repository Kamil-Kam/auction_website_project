from django.urls import path, include
from .views import *


urlpatterns = [
    path('conditions/', Conditions.as_view(), name='conditions'),
    path('categories/', Categories.as_view(), name='categories'),

    path('user/create/', UserCreate.as_view(), name='user/create'),
    path('user/login/', UserLogin.as_view(), name='user/login'),
    path('user/delete/', UserDelete.as_view(), name='user/delete'),
    path('user/logged_in/', UserLoggedIn.as_view(), name='user/logged_in'),
    path('user/logout/', UserLogout.as_view(), name='user/logout'),
    path('user/avatar/', UserAvatar.as_view(), name='user/avatar'),

    path('items/', Items.as_view(), name='items'),
    path('category/<str:category_name>/items', SingleCategoryItems.as_view(), name='category/items'),
    path('items/yours', ItemsYours.as_view(), name='items/yours'),
    path('items/newest', ItemsNewest.as_view(), name='items/newest'),
    path('item/add', ItemAddView.as_view(), name='item/add'),
    path('item/view/<str:item_id>', ItemView.as_view(), name='item/view'),
    path('item/delete/<str:item_id>', ItemDelete.as_view(), name='item/delete'),
]

