from django.urls import path, include
from .views import *


urlpatterns = [
    path('conditions/', Conditions.as_view(), name='conditions'),
    path('categories/', Categories.as_view(), name='categories'),

    path('user/create/', UserCreate.as_view(), name='user/create'),  # create, update, delete
    path('user/login/', UserLogin.as_view(), name='user/login'),
    path('user/logged_in/', UserLoggedIn.as_view(), name='user/logged_in'),
    path('user/logout/', UserLogout.as_view(), name='user/logout'),

    path('items/', Items.as_view(), name='items'),
    path('item/add/', ItemAddView.as_view(), name='item/add'),  # create, update, delete
    path('item/view/<str:item_id>/', ItemView.as_view(), name='item/view'),
]

