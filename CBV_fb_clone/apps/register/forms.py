from django import forms
from django.contrib.auth.forms import UserCreationForm
from register.models import *

class CustomUserForm(UserCreationForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class':'form-control'}))  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class':'form-control'}))  
    class Meta:
        model = CustomUser
        # fields = '__all__'
        fields = ["username",'first_name','last_name',\
            'email','mobile','DOB',\
                'gender',"password1"]
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'},),
            'first_name': forms.TextInput(attrs={'class':'form-control'},),
            'last_name': forms.TextInput(attrs={'class':'form-control'},),
            'email': forms.TextInput(attrs={'class':'form-control'},),
            'mobile': forms.TextInput(attrs={'class':'form-control'},),
            # 'gender': forms.TextInput(attrs={'class':'form-select'},),
            'DOB': forms.DateInput(attrs={'type': 'date','class':'form-control'},),
            }