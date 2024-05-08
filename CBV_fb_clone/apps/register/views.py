from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.contrib.auth import views
from django.conf import settings

#------Custom single-----------------
from django.dispatch import Signal, receiver

# Define a custom signal
hello_signal = Signal()

@receiver(hello_signal)
def my_signal(sender,instance, **kwargs):
    message = kwargs.get("message")
    print(f"Received signal from {instance.username}: {message}")

hello_signal.send(sender=None,instance=CustomUser.objects.all().first() ,message="Custom Signal form view's : Hello, u r logged in")
#---------------------------------------------------------

class register(generic.CreateView):
    form_class = CustomUserForm
    template_name = 'registration/register.html'
    success_url = '/accounts/login/'

class profile(generic.TemplateView):
    template_name='post/dashboard.html'
    

    
#     def logout_then_login(self,request, login_url='/accounts/login/'):
#         """
#         Log out the user if they are logged in. Then redirect to the login page.
#         """
#         super().dispatch(request)  # Call the parent class method to handle logout
#         return redirect(resolve(login_url))
    
# class user_login(generic.View):
#     form_class = AuthenticationForm
#     template_name = 'registration/login.html'    
#     def get(self,request):
#         form = self.form_class
#         return render(request, self.template_name, {'form':form})
    
#     def post(self,request):
#         fm = AuthenticationForm(request=request,data = request.POST)
#         if fm.is_valid():
#             username = fm.cleaned_data.get('username')
#             password = fm.cleaned_data.get('password')
#             if user := authenticate(username = username, password = password):
#                 login(request,user)
#                 return redirect('Register:profile')
#         else:
#             fm = AuthenticationForm(request.POST)
#         return render(request,'registration/login.html',{'form':fm,'message':'try again!!!'})
    

# class user_logout(generic.View):
#     def get(self,request):
#         logout(request)
#         return redirect('/')
