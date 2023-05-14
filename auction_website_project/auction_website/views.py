from django.shortcuts import render, redirect
from .models import Category, Item, Account, Condition
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404


# Create your views here.


def main_page(request, username):
    account = Account.objects.get(username=username)

    context = {
        'account': account
    }

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


def add_item(request):

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

        item = Item(
            description=description,
            title=title,
            price=price,
            category=Category.objects.get(category=category),
            condition=Condition.objects.get(condition=condition),
            location=location,
            amount=amount,
        )

        try:
            item.full_clean()
            item.save()
            message = 'Item added'

            return render(request, "add_item.html", {'categories': categories, 'conditions': conditions,
                                                      'message': message})

        except ValidationError as error:
            errors = list(error.messages)
            print(errors)

            return render(request, "add_item.html", {'categories': categories, 'conditions': conditions,
                                                     "error_message": errors, 'description': description,
                                                     'title': title, 'price': price,
                                                     'category': category, 'condition': condition,
                                                     'location': location, 'amount': amount})

    context = {'categories': categories, 'conditions': conditions}

    return render(request, 'add_item.html', context)


def item_view(request):
    return render(request, 'item_view.html')


def item_photo(request):
    return render(request, 'item_photo.html')


def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            account = Account.objects.get(username=username)

            if check_password(password, account.password):
                messages.success(request, "Logged In Sucessfully!")

                return redirect("main_page", username=username)

            else:
                messages.error(request, 'Invalid username or password')

        except:
            messages.error(request, 'Invalid username or password')

    return render(request, 'log_in.html')


def account(request, username):
    account = get_object_or_404(Account, username=username)

    if request.method == 'POST':

        if 'avatar' in request.POST:
            account.avatar = request.POST['avatar']
            account.save()
            print('sdasd')
            return render(request, "account.html", {'account': account})

        elif 'email' in request.POST:

            account.email = request.POST['email']
            account.username = request.POST['username']
            account.firstname = request.POST['firstname']
            account.surname = request.POST['surname']
            account.country = request.POST['country']
            account.city = request.POST['city']
            account.street = request.POST['street']
            account.postcode = request.POST['postcode']

            try:
                account.full_clean()
                account.save()

                return redirect("account", username=account.username)

            except ValidationError as error:
                errors = list(error.messages)
                print('error')

                return render(request, "account.html", {"error_message": errors, 'account': account})

        elif 'old_password' in request.POST:
            old_password = request.POST['old_password']

            if check_password(old_password, account.password):
                password = request.POST['password']
                repeated_password = request.POST['repeated_password']

                try:

                    if password != repeated_password:
                        raise ValidationError("Passwords do not match")

                    if not validators.validate_password(password):
                        raise ValidationError("Wrong password")

                    account.password = make_password(password)
                    account.full_clean()
                    account.save()

                    return render(request, "account.html", {'account': account})

                except ValidationError as error:
                    errors = list(error.messages)
                    print('error')

                    if not validators.validate_password(password):
                        errors.append("Wrong password")

                    if password != repeated_password:
                        errors.append("Passwords do not match")

                    return render(request, "account.html", {"error_message": errors, 'account': account})

            else:
                return render(request, "account.html", {"error_message": ['wrong old password'], 'account': account})

        return render(request, 'account.html', {'account': account})

    else:
        return render(request, 'account.html', {'account': account})


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

        try:
            account.full_clean()

            if password != repeated_password:
                raise ValidationError("Passwords do not match")

            if not validators.validate_password(password):
                raise ValidationError("Wrong password")

            account.save()

            return redirect("account", username=account.username)

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
