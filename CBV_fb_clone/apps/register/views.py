from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic

class register(generic.CreateView):
    form_class = CustomUserForm
    template_name = 'register/register.html'
    success_url = '/'
    
class user_login(generic.View):
    form_class = AuthenticationForm
    template_name = 'register/login.html'    
    def get(self,request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    
    def post(self,request):
        fm = AuthenticationForm(request=request,data = request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            password = fm.cleaned_data.get('password')
            if user := authenticate(username = username, password = password):
                login(request,user)
                return redirect('Post:dashboard')
        else:
            fm = AuthenticationForm(request.POST)
        return render(request,'register/login.html',{'form':fm,'message':'try again!!!'})
    

class user_logout(generic.View):
    def get(self,request):
        logout(request)
        return redirect('/')
