from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Dangky(forms.Form):
    username = forms.CharField(label = 'Tên tài khoản',max_length=20)
    email = forms.EmailField(label = 'Email')
    pass1 = forms.CharField(label = 'Mật khẩu',widget=forms.PasswordInput)
    pass2 = forms.CharField(label='Nhập lại mật khẩu',widget=forms.PasswordInput)
    def clean_pass2(self):
        if 'pass1' in self.cleaned_data:
            pass1 = self.cleaned_data['pass1']
            pass2 =self.cleaned_data['pass2']
            if pass1==pass2 and pass1:
                return pass2
        raise forms.ValidationError('Mật khẩu không hợp lệ')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$',username): #nếu có kí tự đặcbiệt trong username
            raise forms.ValidationError('Tài khoản có kí tự đặc biệt')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Tài khoản đã tồn tại')

    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'] , email=self.cleaned_data['email'],
                                 password=self.cleaned_data['pass2'])

class DangNhap(forms.ModelForm):
    pass