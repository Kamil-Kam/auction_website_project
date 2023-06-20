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
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'country',
                  'city', 'street', 'postcode', 'password', 'repeated_password', 'avatar']

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

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.street = validated_data.get('street', instance.street)
        instance.postcode = validated_data.get('postcode', instance.postcode)
        instance.password = validated_data.get('password', instance.password)
        instance.avatar = validated_data.get('avatar')

        instance.full_clean()
        instance.save()

        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

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

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        instance.category = Category.objects.get(id=validated_data.get('category', instance.category.id))
        instance.condition = Condition.objects.get(id=validated_data.get('condition', instance.condition.id))
        instance.location = validated_data.get('location', instance.location)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.main_image = validated_data.get('main_image', instance.main_image)

        instance.full_clean()
        instance.save()

        images = validated_data.get('images')
        if images:
            instance.images.all().delete()

            for image in images:
                item_photo = ItemPhoto.objects.create(image=image)
                instance.images.add(item_photo)

        return instance


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

