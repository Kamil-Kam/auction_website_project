from django.shortcuts import render, redirect
from . models import Category, Item, Account

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

    return render(request, 'log_in.html')


def account(request):

    return render(request, 'account.html')


def create_account(request):

    if request.method == 'POST':
        Account.objects.create(
            email=request.POST['email'],
            username=request.POST['username'],
            firstname=request.POST['firstname'],
            surname=request.POST['surname'],
            country=request.POST['country'],
            city=request.POST['city'],
            street=request.POST['street'],
            postcode=request.POST['postcode'],
            password=request.POST['password'],
        )

    return render(request, "create_account.html")



