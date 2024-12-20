from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.exceptions import ValidationError

# Create your models here.
class Profile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  phone = models.CharField(max_length=20, blank=True, null=True)
  bank = models.CharField(max_length=100, blank=True)
  card_number = models.CharField(max_length=20, blank=True)
  old_cart = models.CharField(max_length=200, blank=True, null=True)

  def __str__(self):
    return self.user.username


class Category(models.Model):
  name = models.CharField(max_length=30)
  slug = models.SlugField(max_length=30)
  
  def __str__(self):
    return self.name
  
  
class Element(models.Model):
  name = models.CharField(max_length=40)
  slug = models.SlugField(max_length=40)
  
  def __str__(self):
    return self.name
  
  

class Product(models.Model):
  title = models.CharField(max_length=200)
  slug = models.SlugField(max_length=200, blank=True, null=True)
  category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
  element = models.ForeignKey(Element, null=True, on_delete=models.SET_NULL, blank=True)
  description = models.TextField()
  img1 = models.URLField(max_length=500)
  img2 = models.URLField(max_length=500, blank=True, null=True)
  img3 = models.URLField(max_length=500, blank=True, null=True)
  img4 = models.URLField(max_length=500, blank=True, null=True)
  price = models.DecimalField(max_digits=10, decimal_places=0)
  is_sale = models.BooleanField(default=False)
  discount = models.DecimalField(decimal_places=0, max_digits=3, blank=True, null=True)
  sale_price = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
  start_sale = models.DateField(blank=True, null=True)
  end_sale = models.DateField(blank=True, null=True)
  quantity = models.IntegerField(default=30)
  q_purchase = models.IntegerField(default=0)
  stock = models.IntegerField(null=True, blank=True)
  status = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True)

  def clean(self):
    if not self.is_sale and (self.start_sale or self.end_sale or self.discount):
      raise ValidationError("Không thể nhập `start_sale` và `end_sale` khi `is_sale` là False.")
  
  def save(self, *args, **kwargs):
    self.stock = self.quantity - self.q_purchase
    if self.stock <= 5:
        self.status = False
    if not self.slug:
      self.slug = slugify(self.title)
    if self.discount and not self.sale_price:
      self.sale_price = self.price - (self.discount / 100) * self.price
    self.clean()
    super(Product, self).save(*args, **kwargs)

    
  def __str__(self):
    return self.title