from rest_framework import serializers
from .models import Category, Condition, CustomUser, Item, ItemPhoto
from django.contrib.auth import authenticate, login


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']


class ConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ['id', 'condition']


class ItemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPhoto
        fields = ['id', 'image']


class ItemsSerializer(serializers.ModelSerializer):
    images = ItemPhotoSerializer(many=True)

    class Meta:
        model = Item
        fields = ['id', 'description', 'title', 'price', 'category', 'condition', 'location',
                  'amount', 'user_seller', 'images', 'created_data', 'main_image']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    repeated_password = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'country',
                  'city', 'street', 'postcode', 'password', 'repeated_password']

    def validate(self, attrs):
        password = attrs.get('password')
        repeated_password = attrs.get('repeated_password')

        if password != repeated_password:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

    def create(self, validated_data):

        user = CustomUser(**validated_data)
        user.full_clean()
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user:
            attrs['user'] = user
            return attrs

        else:
            raise serializers.ValidationError("Invalid username or password.")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'country',
                  'city', 'street', 'postcode']

