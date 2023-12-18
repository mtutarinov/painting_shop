from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Painting
from cart.cart import Cart

menu = [
    # {'title': 'О художнике', 'url_name': ''},
    {'title': 'Магазин', 'url_name': 'paintings'},
    {'title': 'Контакты', 'url_name': 'contacts'}
]


def about(request):
    return render(request, 'shop/painting/about.html', {'menu': menu})


def contacts(request):
    return render(request, 'shop/painting/contacts.html', {'menu': menu})


def painting_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    paintings = Painting.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        paintings = paintings.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'paintings': paintings,
        'menu': menu,
    }
    return render(request, 'shop/painting/list.html', context=context)


def painting_detail(request, id, slug):
    painting = get_object_or_404(Painting, id=id, slug=slug)
    return render(request, 'shop/painting/detail.html', {'painting': painting, 'menu': menu})


