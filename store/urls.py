from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('register/', views.register, name='register'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('account/', views.account, name='account'), 
  path('update-info/', views.update_info, name = 'update-info'), 
  path('collections/all/', views.products, name='all'),
  path('collections/bo-suu-tap-moi/', views.new_product, name='new-product'),
  path('collections/<slug:cat_ele>/', views.cat_ele, name='cat-ele'),
  path('products/<slug:slug_product>/', views.product_detail, name='product-detail'),
  path('search/', views.search, name='search')
]