from django.shortcuts import render
from . import models

# Create your views here.


def main_page(request):

    return render(request, 'main_page.html')


def categories_view(request):

    return render(request, 'categories_view.html')


def single_category(request):

    return render(request, 'single_category.html')


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



