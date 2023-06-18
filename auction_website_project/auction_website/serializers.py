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


class ItemSerializer(serializers.ModelSerializer):
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
                  'city', 'street', 'postcode', 'avatar']


class AvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField()


class ItemCreateSerializer(serializers.Serializer):
    description = serializers.CharField()
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    category = serializers.CharField()
    condition = serializers.CharField()
    location = serializers.CharField()
    amount = serializers.IntegerField()
    main_image = serializers.ImageField()
    images = serializers.ListField(child=serializers.ImageField())

    def create(self, validated_data):
        user = self.context['request'].user
        item = Item(
            description=validated_data['description'],
            title=validated_data['title'],
            price=validated_data['price'],
            category=Category.objects.get(id=validated_data['category']),
            condition=Condition.objects.get(id=validated_data['condition']),
            location=validated_data['location'],
            amount=validated_data['amount'],
            user_seller=user,
            main_image=validated_data['main_image']
        )

        item.full_clean()
        item.save()

        images = validated_data.get('images')
        if images:
            for image in images:
                item_photo = ItemPhoto.objects.create(image=image)
                item.images.add(item_photo)



class ItemViewSerializer(serializers.ModelSerializer):
    images = ItemPhotoSerializer(many=True)

    class Meta:
        model = Item
        fields = ['description', 'title', 'price', 'category', 'condition',
                  'location', 'amount', 'main_image', 'images', 'created_data']



class AvatarSerializer(serializers.Serializer):
    avatar = serializers.ImageField()

    def validat(self, value):

        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('Avatar file size exceeds the limit')

        max_width = 500
        max_height = 500
        if value.width > max_width or value.height > max_height:
            raise serializers.ValidationError('Avatar dimensions exceed the limit')

        return value

