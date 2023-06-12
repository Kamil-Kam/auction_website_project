from django.urls import path
from .views import *
from .views_test import *


urlpatterns = [
    path('account', account, name='account'),
    path('add_item', add_item, name='add_item'),
    path('categories_view', categories_view, name='categories_view'),
    path('item_photo', item_photo, name='item_photo'),
    path('log_in', log_in, name='log_in'),
    path('', main_page, name='main_page'),
    path('single_category/<str:category_name>/', single_category, name='single_category'),
    path('item_view/<int:item_id>/', item_view, name='item_view'),
    path('create_account', create_account, name='create_account'),
    path('your_offers', your_offers, name='your_offers'),
    path('delete_user', delete_user, name='delete_user'),
    path('delete_item/<int:item_id>/', delete_item, name='delete_item'),
    path('edit_item/<int:item_id>/', edit_item, name='edit_item'),
    path('delete_photo/<int:item_id>/<int:photo_id>/', delete_photo, name='delete_photo'),

    path('api/categories/', CategoryList.as_view(), name='category-list'),
    path('api/conditions/', ConditionList.as_view(), name='condition-list'),
    path('api/users/', CustomUserList.as_view(), name='user-list'),
    path('api/items/', ItemList.as_view(), name='item-list'),

    path('api/items/newest', ItemsNewestAPIView.as_view(), name='items/newest'),
    path('api/categories/', CategoriesAPIView.as_view(), name='categories'),
    path('api/category/<str:category_name>/', CategoryAPIView.as_view(), name='category'),
    path('api/user/create/', UserCreateAPIView.as_view(), name='user/create'),
    path('api/user/login/', UserLoginAPIView.as_view(), name='user/login'),
    path('api/user/delete/', UserDeleteAPIView.as_view(), name='user/delete'),
]
