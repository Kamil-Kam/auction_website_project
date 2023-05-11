from django.shortcuts import render, redirect
from . models import Category, Item, Account
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import NewUAccountForm
from . import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.


def main_page(request):

    return render(request, 'main_page.html')


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


def add_item(request):

    return render(request, 'add_item.html')


def item_view(request):

    return render(request, 'item_view.html')


def item_photo(request):

    return render(request, 'item_photo.html')


def log_in(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # user = authenticate(request, username=username, password=password)
        print(password)

        try:
            user = Account.objects.get(username=username)
            print(user.password)
            if check_password(password, user.password):
                messages.success(request, "Logged In Sucessfully!")

            else:
                messages.error(request, 'Invalid username or password')

        except:
            messages.error(request, 'Invalid username or password')


    return render(request, 'log_in.html')


def account(request):

    return render(request, 'account.html')


def create_account(request):

    if request.method == 'POST':

        email = request.POST['email']
        username = request.POST['username']
        firstname = request.POST['firstname']
        surname = request.POST['surname']
        country = request.POST['country']
        city = request.POST['city']
        street = request.POST['street']
        postcode = request.POST['postcode']
        password = request.POST['password']
        repeated_password = request.POST['repeated_password']
        print(password)
        account = Account(
            email=email,
            username=username,
            firstname=firstname,
            surname=surname,
            country=country,
            city=city,
            street=street,
            postcode=postcode,
            password=make_password(password),
        )
        print(account.password)
        try:
            account.full_clean()

            if password != repeated_password:
                raise ValidationError("Passwords do not match")

            if not validators.validate_password(password):
                raise ValidationError("Wrong password")

            account.save()

            return render(request, "account.html", {"account": account})

        except ValidationError as error:
            errors = list(error.messages)
            print('error')

            if not validators.validate_password(password):
                errors.append("Wrong password")

            if password != repeated_password:
                errors.append("Passwords do not match")

            return render(request, "create_account.html", {"error_message": errors, "email": email,
                                                           "username": username, "firstname": firstname,
                                                           "surname": surname, "country": country, "city": city,
                                                           "street": street, "postcode": postcode})

    return render(request, "create_account.html")



