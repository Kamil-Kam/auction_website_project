from django.urls import path
from .views import *


urlpatterns = [
    path('api/conditions/', Conditions.as_view(), name='conditions'),
    path('api/items/', Items.as_view(), name='items'),
    path('api/categories/', Categories.as_view(), name='categories'),

    path('api/items/newest', ItemsNewest.as_view(), name='items/newest'),
    path('api/category/<str:category_name>/items', SingleCategoryItems.as_view(), name='category/items'),

    path('api/user/create/', UserCreate.as_view(), name='user/create'),
    path('api/user/login/', UserLogin.as_view(), name='user/login'),
    path('api/user/delete/', UserDelete.as_view(), name='user/delete'),
    path('api/user/logged_in/', UserLoggedIn.as_view(), name='user/logged_in'),
    path('api/user/logout/', UserLogout.as_view(), name='user/logout'),
]
