from . import views
from django.urls import path
from django.urls import path
from .views import *


urlpatterns = [
    path('account', views.account, name='account'),
    path('add_item', views.add_item, name='add_item'),
    path('categories_view', views.categories_view, name='categories_view'),
    path('item_photo', views.item_photo, name='item_photo'),
    path('log_in', views.log_in, name='log_in'),
    path('', views.main_page, name='main_page'),
    path('single_category/<str:category_name>/', views.single_category, name='single_category'),
    path('item_view/<int:item_id>/', views.item_view, name='item_view'),
    path('create_account', views.create_account, name='create_account'),
    path('your_offers', views.your_offers, name='your_offers'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete_photo/<int:item_id>/<int:photo_id>/', views.delete_photo, name='delete_photo'),

    path('api/categories/', CategoryList.as_view(), name='category-list'),
    path('api/conditions/', ConditionList.as_view(), name='condition-list'),
    path('api/users/', CustomUserList.as_view(), name='user-list'),
    path('api/items/', ItemList.as_view(), name='item-list'),

    path('api/main_page/', MainPageAPIView.as_view(), name='main_page'),
    path('api/categories/', CategoriesAPIView.as_view(), name='categories')
]
