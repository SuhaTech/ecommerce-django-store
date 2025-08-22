from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Cart endpoints (AJAX)
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<slug:slug>/', views.cart_add, name='cart_add'),
    path('cart/set/<slug:slug>/', views.cart_set, name='cart_set'),
    path('cart/remove/<slug:slug>/', views.cart_remove, name='cart_remove'),

    # Checkout & Invoice
    path('checkout/', views.checkout, name='checkout'),
    path('invoice/', views.invoice, name='invoice'),  # ✅ fixed
]
