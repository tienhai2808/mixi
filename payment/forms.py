from django import forms
from .models import ShippingAddress

class ShippingForm(forms.ModelForm):
  PAYMENT_CHOICES = [('cash', 'Thanh Toán Khi Nhận Hàng'), ('card', 'Thanh Toán Chuyển Khoản Ngân Hàng'),]
  shipping_full_name = forms.CharField(label="Họ tên", widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
  shipping_phone = forms.CharField(label="Số điện thoại", widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
  shipping_address = forms.CharField(label="Địa chỉ", widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
  shipping_city = forms.CharField(label="Thành phố", widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
  shipping_state = forms.CharField(label="Tỉnh", widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
  shipping_payment_type = forms.ChoiceField(label="", choices=PAYMENT_CHOICES, widget=forms.RadioSelect(attrs={'id':'payment-type'}), initial='cash', required=False)
  shipping_card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'id':'card-form'}), required=False)
  shipping_bank = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'id':'card-form'}), required=False)
  
  class Meta: 
    model = ShippingAddress
    exclude = ['user', ]