from . import views
from django.urls import path


urlpatterns = [
    path('account', views.account, name='account'),
    path('add_item', views.add_item, name='add_item'),
    path('categories_view', views.categories_view, name='categories_view'),
    path('item_photo', views.item_photo, name='item_photo'),
    path('log_in', views.log_in, name='log_in'),
    path('', views.main_page, name='main_page'),
    path('single_category/<str:category_name>/', views.single_category, name='single_category'),
    path('item_view', views.item_view, name='item_view'),
    path('create_account', views.create_account, name='create_account'),
    path('your_offers', views.your_offers, name='your_offers'),
    path('delete_user', views.delete_user, name='delete_user'),
    path('delete_item', views.delete_item, name='delete_item'),
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
]
