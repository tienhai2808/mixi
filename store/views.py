from django.shortcuts import render, redirect
from .forms import SignUpForm, SignInForm, UserInfoForm
from .models import Profile, Product, Category, Element
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.utils import Cart
import json
from payment.models import ShippingAddress
from payment.forms import ShippingForm

# Create your views here.
def home(request):
  title = 'MIXI.VN - Trang sức đá phong thủy MIXI - Trang sức đá tự nhiên'
  context = {'title': title}
  return render(request, 'pages/home.html', context)

def account(request):
  try:
    user = User.objects.get(id=request.user.id)
  except User.DoesNotExist:
    user = None
  if user:
    title = f'{request.user.first_name} {request.user.last_name}'
    context = {'title': title}
    return render(request, 'pages/account.html', context)
  else:
    messages.warning(request, 'Đã đăng nhập đéo đâu')
    return redirect('login')

def update_info(request):
  title = 'Chỉnh Sửa Thông Tin'
  if request.user.is_authenticated:
    current_user = Profile.objects.get(user__id = request.user.id)
    shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
    form = UserInfoForm(request.POST or None, instance=current_user)
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    
    if form.is_valid() or shipping_form.is_valid():
      form.save()
      shipping_form.save()
      messages.success(request, 'Sửa Thông Tin Thành Công')
      return redirect('account')
    context = {'title': title, 
               'form': form , 
               'shipping_form': shipping_form}
    return render (request, 'pages/update_info.html', context)
  else: 
    return redirect('/')

def register(request):
  title = 'Đăng ký'
  form_su = SignUpForm()
  if request.POST:
    form_su = SignUpForm(request.POST)
    if form_su.is_valid():
      user = form_su.save()
      profile = Profile.objects.create(user = user, phone=form_su.cleaned_data['phone'])
      profile.save()
      return redirect('login')
  context = {'title': title,
             'form_su': form_su}
  return render(request, 'pages/register.html', context)

def login(request):
  title = 'Đăng nhập'
  form_si = SignInForm()
  if request.user.is_authenticated:
    messages.error(request, 'Bạn đã đăng nhập')
    return redirect('account')
  if request.POST:
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None: 
        auth.login(request, user)
        current_user = Profile.objects.get(user__id =request.user.id)
        save_cart = current_user.old_cart
        if save_cart:
          convert_cart = json.loads(save_cart)
          cart = Cart(request)
          for key, value in convert_cart.items():
            cart.db_add(product=key, quantity=value)
        return redirect('/')
    else:
        messages.error(request, 'Tài khoản hoặc mật khẩu không đúng')
        return redirect('login')
  context = {'title': title, 
             'form_si': form_si}
  return render(request, 'pages/login.html', context)

def logout(request):
  auth.logout(request)
  return redirect('/')

def products(request):
  title = 'Tất cả sản phẩm'
  products = Product.objects.filter(status=True)
  sort_by = request.GET.get('sort_by')
  if sort_by == 'price-ascending':
    products = products.order_by('price')
  elif sort_by == 'price-descending':
    products = products.order_by('-price')
  elif sort_by == 'title-ascending':
    products = products.order_by('title')
  elif sort_by == 'title-descending':
    products = products.order_by('-title') 
  elif sort_by == 'created-ascending':
    products = products.order_by('created_at')
  elif sort_by == 'created-descending':
    products = products.order_by('-created_at')
  elif sort_by == 'best-selling':
    products = products.annotate(total_q_purchase=Sum('q_purchase')).order_by('-total_q_purchase')
  elif sort_by == 'quantity-descending':
    products = products.annotate(total_stock = Sum('stock')).order_by('-total_stock')
  else:
    products = products.order_by('?')
  paginator = Paginator(products, 5)
  page_number = request.GET.get('page', '')
  try:
    page_obj = paginator.get_page(page_number)
  except PageNotAnInteger:
    page_obj = paginator.page(1)
  except EmptyPage:
    page_obj = paginator.page(paginator.num_pages)
  query_params = request.GET.copy()
  if 'page' in query_params:
    query_params.pop('page')
  context = {'title': title,
             'sort_by': sort_by,
             'page_obj': page_obj,
             'query_params': query_params.urlencode()}
  return render(request, 'pages/products.html', context)

def new_product(request):
  title = 'Bộ sưu tập mới'
  products = Product.objects.filter(status=True).order_by('-created_at')
  sort_by = request.GET.get('sort_by')
  if sort_by == 'price-ascending':
    products = products.order_by('price')
  elif sort_by == 'price-descending':
    products = products.order_by('-price')
  elif sort_by == 'title-ascending':
    products = products.order_by('title')
  elif sort_by == 'title-descending':
    products = products.order_by('-title') 
  elif sort_by == 'created-ascending':
    products = products.order_by('created_at')
  elif sort_by == 'created-descending':
    products = products.order_by('-created_at')
  elif sort_by == 'best-selling':
    products = products.annotate(total_q_purchase=Sum('q_purchase')).order_by('-total_q_purchase')
  elif sort_by == 'quantity-descending':
    products = products.annotate(total_stock = Sum('stock')).order_by('-total_stock')
  else:
    products = products.order_by('-created_at')
  paginator = Paginator(products, 5)
  page_number = request.GET.get('page', '')
  try:
    page_obj = paginator.get_page(page_number)
  except PageNotAnInteger:
    page_obj = paginator.page(1)
  except EmptyPage:
    page_obj = paginator.page(paginator.num_pages)
  query_params = request.GET.copy()
  if 'page' in query_params:
    query_params.pop('page')
  context = {'title': title,
             'page_obj': page_obj,
             'sort_by': sort_by,
             'query_params': query_params.urlencode()}
  return render(request, 'pages/new_product.html', context)

def cat_ele(request, cat_ele):
  try:
    cat = Category.objects.get(slug=cat_ele)
  except Category.DoesNotExist:
    cat = None
  try:
    ele = Element.objects.get(slug=cat_ele)
  except Element.DoesNotExist:
    ele = None
  if cat:
    title = cat.name
    products = Product.objects.filter(category=cat, status=True)
  elif ele:
    title = ele.name
    products = Product.objects.filter(element=ele, status=True)
  else:
    return redirect('all')
  sort_by = request.GET.get('sort_by')
  if sort_by == 'price-ascending':
    products = products.order_by('price')
  elif sort_by == 'price-descending':
    products = products.order_by('-price')
  elif sort_by == 'title-ascending':
    products = products.order_by('title')
  elif sort_by == 'title-descending':
    products = products.order_by('-title') 
  elif sort_by == 'created-ascending':
    products = products.order_by('created_at')
  elif sort_by == 'created-descending':
    products = products.order_by('-created_at')
  elif sort_by == 'best-selling':
    products = products.annotate(total_q_purchase=Sum('q_purchase')).order_by('-total_q_purchase')
  elif sort_by == 'quantity-descending':
    products = products.annotate(total_stock = Sum('stock')).order_by('-total_stock')
  else:
    products = products.order_by('?')
  paginator = Paginator(products, 5)
  page_number = request.GET.get('page', '')
  try:
    page_obj = paginator.get_page(page_number)
  except PageNotAnInteger:
    page_obj = paginator.page(1)
  except EmptyPage:
    page_obj = paginator.page(paginator.num_pages)
  query_params = request.GET.copy()
  if 'page' in query_params:
    query_params.pop('page')
  context = {'title': title,
             'sort_by': sort_by,
             'page_obj': page_obj,
             'query_params': query_params.urlencode()}
  return render(request, 'pages/collection.html', context)

def product_detail(request, slug_product):
  try:
    product = Product.objects.get(slug=slug_product, status=True)
  except Product.DoesNotExist:
    product = None
  if product:
    title = product.title
    care_products = []
    if product.element:
      for pro in product.category.product_set.exclude(id=product.id)[:4]:
        care_products.append(pro)
      for pro in product.element.product_set.exclude(id=product.id)[:3]:
        if pro not in care_products:
          care_products.append(pro)
    else:
      care_products = product.category.product_set.exclude(id=product.id)[:6]
    context = {'title': title,
               'product': product,
               'care_products': care_products}
    return render(request, 'pages/product_detail.html', context)
  else:
    messages.warning(request, 'Không tìm thấy sản phẩm này')
    return redirect('/')
  
def search(request):
  q = request.GET.get('q', '')
  if q:
    title = f"Kết quả tìm kiếm '{q}'"
    products = Product.objects.filter(title__icontains=q, status=True)
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page', '')
    try:
      page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
      page_obj = paginator.page(1)
    except EmptyPage:
      page_obj = paginator.page(paginator.num_pages)
    query_params = request.GET.copy()
    if 'page' in query_params:
      query_params.pop('page')
    context = {'title': title,
              'q': q,
              'page_obj': page_obj,
              'query_params': query_params.urlencode()}
    return render(request, 'pages/search.html', context)
  else:
    return redirect('all')
    
