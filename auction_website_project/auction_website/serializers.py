from rest_framework import serializers
from .models import Category, Condition, CustomUser, Item, ItemPhoto


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']


class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['id', 'condition']


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'country', 'city', 'street', 'postcode', 'avatar']


class ItemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPhoto
        fields = ['id', 'image']


class ItemSerializer(serializers.ModelSerializer):
    images = ItemPhotoSerializer(many=True)

    class Meta:
        model = Item
        fields = ['id', 'description', 'title', 'price', 'category', 'condition', 'location',
                  'amount', 'user_seller', 'images', 'created_data', 'main_image']
