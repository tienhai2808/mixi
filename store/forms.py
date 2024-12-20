from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserInfoForm(forms.ModelForm):
  phone = forms.CharField(label="Số điện thoại", widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
  bank = forms.CharField(label="Tên ngân hàng", widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
  card_number = forms.CharField(label="Số thẻ", widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
  
  class Meta:
    model = Profile
    fields = ('phone', 'bank', 'card_number')


class SignInForm(forms.ModelForm):
	class Meta:
		model=User
		fields = ['username', 'password']
		widgets = {'username': forms.TextInput(attrs={'class': 'form-control'}),
						'password': forms.PasswordInput(attrs={'class': 'form-control'})}
		labels = {'username': 'Tài khoản', 'password': 'Mật khẩu'}


class SignUpForm(UserCreationForm):
	first_name = forms.CharField(label="Họ", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(label="Tên", max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
	phone = forms.CharField(label="Số điện thoại",max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].label = 'Tên đăng nhập'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].label = 'Mật khẩu'
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Mật khẩu phải hơn 8 ký tự.</li><li>Mật khẩu không được toàn số.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].label = 'Nhập lại mật khẩu'
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Nhập lại mật khẩu để xác minh.</small></span>'