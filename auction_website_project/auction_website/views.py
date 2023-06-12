from django.shortcuts import render, redirect
from .models import Category, Item, Condition, CustomUser, ItemPhoto
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ConditionList(generics.ListAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer
    permission_classes = [AllowAny]


class CustomUserList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


class ItemList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]


class ItemsNewestAPIView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        items = list(reversed(Item.objects.order_by('-created_data')))[:5]
        serializer = ItemSerializer(items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoriesAPIView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_name):
        items = Item.objects.filter(category__category=category_name)
        serializer = ItemSerializer(items, many=True)

        return Response(serializer.data)


class UserCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            repeated_password = serializer.validated_data.pop('repeated_password')

            if password != repeated_password:
                return Response({"error_message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save(password=make_password(password))

            return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


class UserDeleteAPIView(APIView):
    @login_required
    def post(self, request):
        user = request.user
        password = request.data.get('password')

        if authenticate(username=user.username, password=password):
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            message = 'Wrong password.'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

