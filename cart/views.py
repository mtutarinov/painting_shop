from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Painting
from .cart import Cart


@require_POST
def cart_add(request, painting_id):
    cart = Cart(request)
    painting = get_object_or_404(Painting, id=painting_id)
    cart.add(request, painting=painting)
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, painting_id):
    cart = Cart(request)
    painting = get_object_or_404(Painting, id=painting_id)
    cart.remove(painting)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
