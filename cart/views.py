from django.shortcuts import render, get_object_or_404, redirect
from .utils import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def cart(request):
  cart = Cart(request)
  title = 'Giỏ Hàng'
  cart_products = cart.get_prods
  quantities = cart.get_quants
  totals = cart.cart_total()
  return render( request, 'pages/cart.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals, 'title': title})

def cart_add(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    product_id = int(request.POST.get('product_id'))
    product_qty = int(request.POST.get('product_qty'))
    product = get_object_or_404(Product, id = product_id)
    cart.add(product = product, quantity = product_qty)
    cart_quantity = cart.__len__()
    response = JsonResponse({'qty': cart_quantity})
    return response

def cart_delete(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    product_id = int(request.POST.get('product_id'))
    cart.delete(product=product_id)
    response = JsonResponse({'product': product_id})
    messages.success(request, ("Xóa sản phẩm khỏi giỏ hàng"))
    return response

def cart_update(request):
  cart = Cart(request)
  if request.POST.get('action') == 'post':
    product_id = int(request.POST.get('product_id'))
    product_qty = int(request.POST.get('product_qty'))
    cart.update(product = product_id, quantity = product_qty)
    response = JsonResponse({'qty': product_qty})
    messages.success(request, ("Cập nhật giỏ hàng thành công"))
    return response
