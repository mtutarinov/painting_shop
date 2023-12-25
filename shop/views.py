from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Painting
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.cart import Cart



def about(request):
    return render(request, 'shop/painting/about.html')


def contacts(request):
    return render(request, 'shop/painting/contacts.html')


def painting_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    painting_list = Painting.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        painting_list = painting_list.filter(category=category)

    paginator = Paginator(painting_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        paintings = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        paintings = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        paintings = paginator.page(paginator.num_pages)
    context = {
        'category': category,
        'categories': categories,
        'paintings': paintings
    }
    return render(request, 'shop/painting/list.html', context=context)


def painting_detail(request, id, slug):
    painting = get_object_or_404(Painting, id=id, slug=slug)
    return render(request, 'shop/painting/detail.html', {'painting': painting})


