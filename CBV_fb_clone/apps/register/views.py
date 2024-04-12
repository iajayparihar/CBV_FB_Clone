from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
def register(request):
    if request.method != 'POST':
        fm = CustomUserForm
        return render(request,'register/register.html',{'form':fm})
    form = CustomUserForm(request.POST)
    if form.is_valid():
        form.save()
        return render(request,'register/register.html',{'form':form,'message':'user created!!!'})
    return render(request,'register/register.html',{'form':form,'message':'form is not valid'})
    
def user_login(request):
    fm = AuthenticationForm()
    if request.method != 'POST':
        return render(request,'register/login.html',{'form':fm})
    fm = AuthenticationForm(request=request,data = request.POST)
    if fm.is_valid():
        username = fm.cleaned_data.get('username')
        password = fm.cleaned_data.get('password')
        if user := authenticate(username = username, password = password):
            login(request,user)
            return render(request,'register/dashboard.html',{'message':'wel-come to dashboard'})
    else:
        fm = AuthenticationForm(request.POST)
    return render(request,'register/login.html',{'form':fm,'message':'try again!!!'})
    
def user_logout(request):
    logout(request)
    return redirect('/')