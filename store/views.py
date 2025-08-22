from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from .models import Product
from decimal import Decimal
import json


@ensure_csrf_cookie
def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'store/product_list.html', {'products': products})


@ensure_csrf_cookie
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'store/product_detail.html', {'product': product})


# ------------------- CART VIEWS -------------------
def cart_add(request, slug):
    """Add product to cart"""
    cart = request.session.get('cart', {})
    qty = int(request.GET.get("qty", 1))

    # update quantity
    if slug in cart:
        cart[slug] += qty
    else:
        cart[slug] = qty

    request.session['cart'] = cart
    return _cart_summary(cart)


def cart_set(request, slug):
    """Update cart quantity (replace instead of add)"""
    cart = request.session.get('cart', {})
    qty = int(request.GET.get("qty", 1))

    if qty > 0:
        cart[slug] = qty
    else:
        cart.pop(slug, None)

    request.session['cart'] = cart
    return _cart_summary(cart)


def cart_remove(request, slug):
    """Remove item from cart"""
    cart = request.session.get('cart', {})
    cart.pop(slug, None)
    request.session['cart'] = cart
    return _cart_summary(cart)


def cart_view(request):
    """Render cart page with items & subtotal"""
    cart = request.session.get('cart', {})
    items, subtotal = _build_cart_items(cart)
    return render(request, 'store/cart.html', {
        "items": items,
        "subtotal": subtotal,
    })


# ------------------- CHECKOUT & INVOICE -------------------
@csrf_exempt  # ✅ avoids CSRF issues on JSON POST
def checkout(request):
    cart = request.session.get("cart", {})

    # calculate cart items
    items, subtotal = _build_cart_items(cart)
    total = subtotal  # adjust if you add tax/shipping later

    if request.method == "POST":
        try:
            # safe JSON parse
            if request.body:
                body = request.body.decode("utf-8")
                data = json.loads(body) if body.strip() else {}
            else:
                data = {}

            # simulate order creation
            if request.user.is_authenticated:
                order_id = f"INV{request.user.id}"
            else:
                order_id = "INV-guest"

            # save order in session for invoice
            request.session["last_order"] = {
                "id": order_id,
                "items": items,
                "subtotal": str(subtotal),
                "total": str(total),
            }

            # clear cart
            request.session["cart"] = {}

            return JsonResponse({
                "success": True,
                "redirect": f"/invoice/"
            })
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    # GET request → render checkout page
    return render(request, "store/checkout.html", {
        "items": items,
        "subtotal": subtotal,
        "total": total,
    })


def invoice(request, order_id=None):
    """Show last order invoice"""
    order = request.session.get("last_order")
    if not order:
        return render(request, "store/no_invoice.html")
    return render(request, "store/invoice.html", {"order": order})


# ------------------- HELPERS -------------------
def _build_cart_items(cart):
    """Convert session cart into product details & subtotal"""
    items = []
    subtotal = Decimal("0.00")

    for slug, qty in cart.items():
        try:
            product = Product.objects.get(slug=slug)
            qty = int(qty)
            line_total = product.price * qty
            subtotal += line_total
            items.append({
                "slug": product.slug,
                "name": product.name,
                "image": product.image.url if product.image else "",
                "price": str(product.price),  # ✅ ensure JSON serializable
                "qty": qty,
                "line_total": str(line_total),  # ✅ ensure JSON serializable
            })
        except (Product.DoesNotExist, ValueError, TypeError):
            continue

    return items, subtotal


def _cart_summary(cart):
    """Return JSON summary of cart"""
    items, subtotal = _build_cart_items(cart)
    cart_count = sum(int(q["qty"]) for q in items)
    return JsonResponse({
        "ok": True,
        "cart_count": cart_count,
        "subtotal": str(subtotal),
    })
def invoice_view(request, order_id):
    order = {
        "id": order_id,
        "items": [
            {"name": "Product A", "quantity": 2, "price": 500, "total": 1000},
            {"name": "Product B", "quantity": 1, "price": 300, "total": 300},
        ],
        "subtotal": 1300,
        "delivery": 50,
        "total": 1350,
    }
    return render(request, "invoice.html", {"order": order})
