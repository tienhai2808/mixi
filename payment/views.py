from django.shortcuts import render, redirect
from cart.utils import Cart
from django.contrib import messages
from .models import ShippingAddress, OrderItem, Order
from .forms import ShippingForm
from django.utils import timezone
from datetime import datetime
from store.models import Product, Profile

# Create your views here.
def order_success(request):
  title = 'Thanh toán thành công'
  context = {'title': title}
  return render(request, 'pages/order_success.html', context)

def checkout(request):
  title = 'Thanh toán'
  cart = Cart(request)
  cart_products = cart.get_prods
  quantities = cart.get_quants
  totals = cart.cart_total()
  if request.user.is_authenticated:
    shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
  else:
    shipping_form = ShippingForm(request.POST or None)
  context = {'cart_products': cart_products, 
              'quantities': quantities, 
              'totals': totals, 
              'shipping_form': shipping_form, 
              'title': title}
  return render(request, 'pages/checkout.html', context)

def billing_info(request):
  if request.POST:
    cart = Cart(request)
    title = 'Thanh toán'
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    my_shipping = request.POST
    request.session['my_shipping'] = my_shipping
    context = {'cart_products': cart_products, 
               'quantities': quantities, 
               'totals': totals, 
               'shipping_info': request.POST, 
               'title': title}
    return render(request, 'pages/billing_info.html', context)
  else:
    return redirect('home')
  
def process_order(request):
  if request.POST:
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    my_shipping = request.session.get('my_shipping')
    full_name = my_shipping['shipping_full_name']
    phone = my_shipping['shipping_phone']
    shipping_address = f"{my_shipping['shipping_address']} - {my_shipping['shipping_city']} - {my_shipping['shipping_state']}"
    payment_method = my_shipping['shipping_payment_type']
    if payment_method == 'card':
      payment_method = 'Thanh Toán Chuyển Khoản Ngân Hàng'
      card_number = my_shipping['shipping_card_number']
      bank = my_shipping['shipping_bank']
    else:
      payment_method = 'Thanh Toán Khi Nhận Hàng'
      card_number = ""
      bank = ""
    amount_paid = totals
    now = timezone.make_aware(datetime.now())
    
    if request.user.is_authenticated:
      user = request.user 
      create_order = Order(user=user, 
                           full_name=full_name, phone=phone, 
                           shipping_address=shipping_address, 
                           payment_method=payment_method, 
                           card_number=card_number, 
                           bank=bank, 
                           amount_paid=amount_paid, 
                           date_ordered=now)
      create_order.save()
      order_id = create_order.pk
      for item in cart_products():
        product_id = item.id
        if item.is_sale:
          price = item.sale_price
        else:
          price = item.price
        for key, value in quantities().items():
          if int(key) == product_id:
            create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price )
            create_order_item.save()
            product = Product.objects.get(id=product_id)
            product.q_purchase += value
            product.save()
      for key in list(request.session.keys()):
        if key == "session_key":
          del request.session[key]
      current_user = Profile.objects.filter(user__id = request.user.id)
      current_user.update(old_cart="")
      messages.success(request, 'Đặt Hàng Thành Công')
      return redirect('order-success')
    else:
      create_order = Order(full_name=full_name, 
                           phone=phone, 
                           shipping_address=shipping_address, 
                           payment_method=payment_method, 
                           card_number=card_number, bank=bank, 
                           amount_paid=amount_paid, 
                           date_ordered=now)
      create_order.save()
      order_id = create_order.pk
      for item in cart_products():
        product_id = item.id
        if item.is_sale:
          price = item.sale_price
        else:
          price = item.price
        for key, value in quantities().items():
          if int(key) == product_id:
            create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price )
            create_order_item.save()
            product = Product.objects.get(id=product_id)
            product.q_purchase += value
            product.save()
      for key in list(request.session.keys()):
        if key == "session_key":
          del request.session[key]
      messages.success(request, 'Đặt Hàng Thành Công')
      return redirect('order-success')
  else:
    return redirect('home')
  
  
def orders(request):
  if not request.user.is_anonymous:
    if request.user.is_superuser:
      title = 'Tất cả đơn hàng'
      orders = Order.objects.all()
    else:
      title = 'Đơn hàng của tôi'
      orders = Order.objects.filter(user=request.user)
    role = 'Quản lý' if request.user.is_superuser else 'Khách hàng'
    status = request.GET.get('status', '')
    if status == 'Tất cả':
      orders = orders.order_by('-date_ordered')
    if status == 'Chờ lấy hàng':
      orders = orders.filter(status='Chờ lấy hàng')
    if status == 'Đã hủy':
      orders = orders.filter(status='Đã hủy')
    if status == 'Đang giao':
      orders = orders.filter(status='Đang giao')
    if status == 'Đã giao':
      orders = orders.filter(status='Đã giao')
    if request.POST:
      action = request.POST.get('action')
      id_order = request.POST.get('id_order')
      order = orders.get(id=id_order)
      if action == 'cancel':
        for item in order.orderitem_set.all():
          product = Product.objects.get(id=item.product.id)
          product.q_purchase -= item.quantity
          product.save()
        order.status = 'Đã hủy'
        order.save()
        messages.success(request, 'Hủy đơn hàng thành công')
      if action == 'shipping':
        order.status = 'Đang giao'
        order.save()
        messages.success(request, 'Đang giao đơn hàng tới khách hàng')
      if action == 'shipped':
        order.status = 'Đã giao'
        order.date_shipped = datetime.now()
        order.save()
        messages.success(request, 'Đã xác nhận giao đơn hàng' if role == 'Quản lý' else 'Đã xác nhận nhận đơn hàng')
    context = {'title': title,
               'orders': orders,
               'role': role,
               'status': status}
    return render(request, 'pages/orders.html', context)
  else:
    return redirect('login')
  
def order(request, pk):
  try:
    order = Order.objects.get(id=pk)
    if order.user == request.user or request.user.is_superuser:
      title = f'Đơn hàng số {pk}'
      role = 'Khách hàng' if order.user == request.user else 'Quản lý'
      if request.POST:
        action = request.POST.get('action')
        if action == 'cancel':
          for item in order.orderitem_set.all():
            product = Product.objects.get(id=item.product.id)
            product.q_purchase -= item.quantity
            product.save()
          order.status = 'Đã hủy'
          order.save()
          messages.success(request, f'Đã hủy đơn hàng số {pk}')
        if action == 'shipping':
          order.status = 'Đang giao'
          order.save()
          messages.success(request, f'Đang giao đơn hàng {pk} tới khách hàng')
        if action == 'shipped':
          order.status = 'Đã giao'
          order.date_shipped = datetime.now()
          order.save()
          messages.success(request, f'Đã nhận đơn hàng {pk}' if role == 'Khách hàng' else f'Đã giao đơn hàng {pk}')
        return redirect("orders")
      context = {'order': order,
                 'role': role, 
                'title': title}
      return render(request, 'pages/order.html', context)
    else:
      return redirect('home')
  except Order.DoesNotExist:
    return redirect('home')
  
