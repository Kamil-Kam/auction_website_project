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


def main_page(request):
    user = request.user
    items = list(reversed(Item.objects.order_by('-created_data')))[:5]

    context = {
        'user': user,
        'items': items,
    }

    if request.method == 'POST':
        if 'log_out' in request.POST:
            logout(request)
            return render(request, 'main_page.html')

    return render(request, 'main_page.html', context)


def categories_view(request):
    categories = Category.objects.all()

    context = {
        'categories': categories,
    }

    return render(request, 'categories_view.html', context)


def single_category(request, category_name):
    items = Item.objects.filter(category__category=category_name)

    context = {
        'category_name': category_name,
        'items': items,
    }

    return render(request, 'single_category.html', context)


@login_required
def add_item(request):
    user = request.user
    categories = Category.objects.all()
    conditions = Condition.objects.all()

    if request.method == 'POST':

        description = request.POST['description']
        title = request.POST['title']
        price = request.POST['price']
        category = request.POST['category']
        condition = request.POST['condition']
        location = request.POST['location']
        amount = request.POST['amount']
        main_image = request.FILES.get('main_image')

        images = request.FILES.getlist('images')

        item = Item(
            description=description,
            title=title,
            price=price,
            category=Category.objects.get(category=category),
            condition=Condition.objects.get(condition=condition),
            location=location,
            amount=amount,
            user_seller=user,
            main_image=main_image,
        )

        try:
            item.full_clean()
            item.save()
            message = 'Item added'

            if images:
                for image in images:
                    item_photo = ItemPhoto.objects.create(image=image)
                    item.images.add(item_photo)

                return render(request, "add_item.html", {'categories': categories, 'conditions': conditions,
                                                            'message': message})

        except ValidationError as error:
            errors = list(error.messages)

            return render(request, "add_item.html", {'categories': categories, 'conditions': conditions,
                                                     "error_message": errors, 'description': description,
                                                     'title': title, 'price': price,
                                                     'category': category, 'condition': condition,
                                                     'location': location, 'amount': amount})

    context = {'categories': categories, 'conditions': conditions}

    return render(request, 'add_item.html', context)


def item_view(request, item_id):
    item = Item.objects.get(id=item_id)

    context = {
        'item': item
    }

    return render(request, 'item_view.html', context)


def item_photo(request):
    return render(request, 'item_photo.html')


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)

            return redirect("main_page")

        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'log_in.html')


@login_required
def account(request):
    user = request.user

    context = {
        'user': user
    }

    if request.method == 'POST':

        if 'avatar' in request.FILES:

            user.avatar = request.FILES.get('avatar')
            user.save()

            return render(request, "account.html", context)

        if 'email' in request.POST:

            user.email = request.POST['email']
            user.username = request.POST['username']
            user.firstname = request.POST['firstname']
            user.surname = request.POST['surname']
            user.country = request.POST['country']
            user.city = request.POST['city']
            user.street = request.POST['street']
            user.postcode = request.POST['postcode']

            try:
                user.full_clean()
                user.save()

                return redirect("account")

            except ValidationError as error:
                errors = list(error.messages)

                return render(request, "account.html", {"error_message": errors, 'user': user})

        elif 'old_password' in request.POST:
            old_password = request.POST['old_password']

            if check_password(old_password, user.password):
                password = request.POST['password']
                repeated_password = request.POST['repeated_password']

                try:
                    if password != repeated_password:
                        raise ValidationError("Passwords do not match")

                    if not validators.validate_password(password):
                        raise ValidationError("Wrong password")

                    user.password = make_password(password)
                    user.full_clean()
                    user.save()

                    return render(request, "account.html", context)

                except ValidationError as error:
                    errors = list(error.messages)

                    if not validators.validate_password(password):
                        errors.append("Wrong password")

                    if password != repeated_password:
                        errors.append("Passwords do not match")

                    return render(request, "account.html", {"error_message": errors, 'user': user})

            else:
                return render(request, "account.html", {"error_message": ['wrong old password'], 'user': user})

        return render(request, 'account.html', {'account': user})

    else:
        return render(request, 'account.html', context)


def create_account(request):
    if request.method == 'POST':

        email = request.POST['email']
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        country = request.POST['country']
        city = request.POST['city']
        street = request.POST['street']
        postcode = request.POST['postcode']
        password = request.POST['password']
        repeated_password = request.POST['repeated_password']

        user = CustomUser(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            country=country,
            city=city,
            street=street,
            postcode=postcode,
            password=make_password(password),
        )

        try:
            user.full_clean()

            if password != repeated_password:
                raise ValidationError("Passwords do not match")

            if not validators.validate_password(password):
                raise ValidationError("Wrong password")

            user.save()
            login(request, user)

            return redirect("account")

        except ValidationError as error:
            errors = list(error.messages)

            if not validators.validate_password(password):
                errors.append("Wrong password")

            if password != repeated_password:
                errors.append("Passwords do not match")

            return render(request, "create_account.html", {"error_message": errors, "email": email,
                                                           "username": username, "first_name": first_name,
                                                           "last_name": last_name, "country": country, "city": city,
                                                           "street": street, "postcode": postcode})

    return render(request, "create_account.html")


@login_required
def your_offers(request):
    user = request.user
    items = Item.objects.filter(user_seller=user)

    context = {
        'items': items
    }

    return render(request, "your_offers.html", context)


@login_required
def delete_user(request):
    user = request.user

    if request.method == 'POST':
        password = request.POST['password']

        if check_password(password, user.password):
            user.delete()

            return redirect('main_page')

        else:
            message = 'wrong password'

            return render(request, 'delete_user.html', {'message': message})

    return render(request, 'delete_user.html')


@login_required
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {
        'item': item
    }

    if request.method == 'POST':
        item.delete()

        return redirect('your_offers')

    return render(request, 'delete_item.html', context)


@login_required
def edit_item(request, item_id):
    item = Item.objects.get(id=item_id)
    categories = Category.objects.all()
    conditions = Condition.objects.all()

    if request.method == 'POST':
        if 'delete_main_image' in request.POST:
            item.main_image.delete()
            item.save()

            context = {
                'categories': categories, 'conditions': conditions, 'item': item
            }

            return render(request, "edit_item.html", context)

        else:
            item.description = request.POST['description']
            item.title = request.POST['title']
            item.price = request.POST['price']
            item.category = Category.objects.get(category=request.POST['category'])
            item.condition = Condition.objects.get(condition=request.POST['condition'])
            item.location = request.POST['location']
            item.amount = request.POST['amount']

            if 'main_image' in request.FILES:
                item.main_image = request.FILES['main_image']

            images = request.FILES.getlist('images')

            try:
                item.full_clean()
                item.save()
                message = 'Item edited'

                if images:
                    for image in images:

                        item_photo = ItemPhoto.objects.create(image=image)
                        item.images.add(item_photo)

                    return render(request, "edit_item.html", {'categories': categories, 'conditions': conditions,
                                                                'message': message, 'item': item})

            except ValidationError as error:
                errors = list(error.messages)

                return render(request, "edit_item.html", {'categories': categories, 'conditions': conditions,
                                                         "error_message": errors, 'item': item})

    context = {
        'categories': categories, 'conditions': conditions, 'item': item
    }
    return render(request, 'edit_item.html', context)


@login_required
def delete_photo(request, item_id, photo_id):
    photo = ItemPhoto.objects.get(id=photo_id)
    photo.delete()

    return redirect('edit_item', item_id=item_id)


