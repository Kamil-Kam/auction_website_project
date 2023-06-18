from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status, viewsets
from .serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .paginations import *

# Create your views here.


class Conditions(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        conditions = Condition.objects.all()
        serializer = ConditionsSerializer(conditions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class Categories(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoriesSerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreate(APIView):
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


class UserLogin(APIView):
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


class UserLoggedIn(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)


class UserDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        password = request.data.get('password')

        if authenticate(username=user.username, password=password):
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            message = 'Wrong password.'
            return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'detail': 'Logout successful.'})


class UserAvatar(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get(self, request):

        user = request.user
        return Response(user.username)

    def post(self, request):
        serializer = AvatarSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            user.avatar = serializer.validated_data['avatar']
            user.save()
            return Response({'detail': 'Avatar uploaded successfully'})

        return Response(serializer.errors, status=400)

    def delete(self, request):
        user = request.user

        if user.avatar:
            user.avatar.delete()
            user.avatar = None
            user.save()

        return Response({'detail': 'Avatar deleted successfully'})


class ItemAddView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = ItemCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Item added'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        item_id = request.data.get('id')

        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            return Response({'detail': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemCreateSerializer(item, data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Item updated'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemView(APIView):

    def get(self, request, item_id):
        item = Item.objects.get(id=item_id)
        serializer = ItemViewSerializer(item)
        return Response(serializer.data)


class Items(APIView):
    permission_classes = [AllowAny]
    pagination_class = ItemPagination

    def get(self, request):

        category = request.query_params.get('category')
        user_seller = request.query_params.get('user_seller')

        if category:
            items = Item.objects.filter(category__category=category)

        elif user_seller:
            items = Item.objects.filter(category__user_seller=user_seller)

        else:
            items = Item.objects.all()

        sort_by = request.query_params.get('sort_by', 'created_date')
        if sort_by == 'price':
            items = items.order_by('price')
        elif sort_by == '-price':
            items = items.order_by('-price')

        if sort_by == 'created_data':
            items = items.order_by('created_data')
        elif sort_by == '-created_data':
            items = items.order_by('-created_data')

        paginator = self.pagination_class()
        paginated_items = paginator.paginate_queryset(items, request)
        serializer = ItemSerializer(paginated_items, many=True)

        return paginator.get_paginated_response(serializer.data)


class ItemDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        user = request.user
        item = Item.objects.get(id=item_id)

        if user == item.user_seller:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
