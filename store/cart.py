from decimal import Decimal
from django.shortcuts import get_object_or_404
from .models import Product

CART_SESSION_ID = 'cart'


def _get_cart(request):
    return request.session.get(CART_SESSION_ID, {})


def _save_cart(request, cart):
    request.session[CART_SESSION_ID] = cart
    request.session.modified = True


def add(request, slug, qty=1):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart = _get_cart(request)

    # Always ensure item is a dict, not int
    item = cart.get(slug)
    if not isinstance(item, dict):
        item = {
            'name': product.name,
            'price': str(product.price),
            'qty': 0,
            'image': product.image.url if product.image else '',
        }

    new_qty = min(int(item['qty']) + int(qty), product.stock)
    item['qty'] = new_qty
    cart[slug] = item

    if item['qty'] <= 0:
        cart.pop(slug, None)

    _save_cart(request, cart)
    return cart


def set_qty(request, slug, qty):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart = _get_cart(request)

    if int(qty) <= 0:
        cart.pop(slug, None)
    else:
        q = min(int(qty), product.stock)
        cart[slug] = {
            'name': product.name,
            'price': str(product.price),
            'qty': q,
            'image': product.image.url if product.image else '',
        }

    _save_cart(request, cart)
    return cart


def remove(request, slug):
    cart = _get_cart(request)
    cart.pop(slug, None)
    _save_cart(request, cart)
    return cart


def clear(request):
    _save_cart(request, {})
    return {}


def summary(request):
    cart = _get_cart(request)
    items = []
    subtotal = Decimal('0.00')

    for slug, data in cart.items():
        # Safety: ensure 'data' is dict
        if not isinstance(data, dict):
            continue

        price = Decimal(data.get('price', '0'))
        qty = int(data.get('qty', 0))
        line_total = price * qty

        items.append({
            'slug': slug,
            'name': data.get('name', ''),
            'price': price,
            'qty': qty,
            'image': data.get('image', ''),
            'line_total': line_total
        })
        subtotal += line_total

    return {
        'items': items,
        'subtotal': subtotal,
        'tax': subtotal * Decimal('0.00'),
        'total': subtotal
    }
