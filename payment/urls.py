from django.urls import path
from . import views

urlpatterns = [
  path('order-success/', views.order_success, name='order-success'),
  path('checkout/', views.checkout, name='checkout'),
  path('billing-info/', views.billing_info, name = 'billing-info'),
  path('process-order/', views.process_order, name='process-order'),
  path('orders/', views.orders, name='orders'),
  path('orders/<int:pk>/', views.order, name='order')
]