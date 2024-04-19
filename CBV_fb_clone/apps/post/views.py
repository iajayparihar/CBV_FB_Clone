from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import generic
from .forms import UserPostForm, UserCommentForm
from .models import *
from django.conf import settings
#--------------------------------------------------------------------------
import requests, os

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
##########################################################################

Email_Api_Key = "AIzaSyDi5Ta4oJtbiBeycRVdGeRcLrxLQhh7atE"
#sending mail
# Abstract Api
def validate_email(email):
    response = requests.get("https://emailvalidation.abstractapi.com/v1/?api_key=371b6bc2168b46838526cbf0eae84649&email=luhulu329@gmail.com")
    data = response.json()
    valueText = data.get('is_valid_format')
    # is_valid_format and is_mx_found and is_smtp_valid and not is_catchall_email and not is_role_email and not is_free_email
    return valueText.get('value')

def send_email(subject, from_email, to_email, reply_to, headers, attechments):
    if validate_email(to_email) and validate_email(reply_to):
        html_message = render_to_string('post/email.html')
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives(
            subject= subject,
            body = plain_message,
            from_email= from_email,
            to=[to_email],
            reply_to= [reply_to],
            headers= headers,
        )
        email.attach_alternative(html_message, "text/html")
        
        img_path = f'{settings.BASE_DIR}/media/user_post/{str(attechments)}'
        
        with open(img_path, 'rb') as file:
            image_data = file.read()
            banner_image = MIMEImage(image_data)
            banner_image.add_header('Content-ID', '<image>')
            email.attach(banner_image)
            email.send()
            
        print('Your emil is sent successfully')
    else:
        print("Invalid recipient email address.")

##########################################################################
class PostFormView(generic.FormView):
    form_class = UserPostForm
    template_name = 'post/post.html'
    success_url = '/post/view_post/'

    # when request.POST then    
    def form_valid(self,form):
        user_post = form.save(commit=False)
        user_post.user = self.request.user            
        user_post.save()
#--------------Email-----------------------------------------------------------------
        subject = "Post Saved"
        headers = {"My-Header": "hello i am header"}
        from_email = settings.EMAIL_HOST_USER
        to_email = "ajayparihar876@gmail.com"
        attachments = form.cleaned_data['image']        
        reply_to = 'ajayparihar876@gmail.com'
        
        send_email(subject=subject,from_email= from_email,to_email= to_email,headers=headers,reply_to=reply_to,attechments=attachments)
#-------------------------------------------------------------------------------
    
        return super().form_valid(form)

#--------------------------------------------------------------------------
class update_post(generic.UpdateView):
    model = UserPost
    form_class = UserPostForm
    template_name = 'post/post.html'
    success_url = '/post/view_post/'
    
#--------------------------------------------------------------------------
class delete_post(generic.DeleteView):
    model = UserPost
    success_url = '/post/view_post/'
    template_name = 'post/conf_delete.html'
    
#--------------------------------------------------------------------------
class all_user_post(generic.ListView):
    model = UserPost
    template_name = 'post/all_user_post.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        all_post = UserPost.objects.all().order_by('-created_at')
        for post in all_post:
            post.is_liked = Like.objects.filter(user=self.request.user,post=post).exists()
        all_cmt = UserComments.objects.all().order_by('-created_at')
        
        # ** always use this type of context pass 
        context['all_user_post'] = all_post
        context['comment'] = all_cmt
    
        return context
        
#--------------------------------------------------------------------------
class view_post(generic.ListView):
    model = UserPost
    template_name = 'post/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_post = UserPost.objects.filter(user=self.request.user).order_by('-created_at')
        all_cmt = UserComments.objects.all().order_by('-created_at')
        for post in user_post:
            post.is_liked = Like.objects.filter(user=self.request.user,post=post).exists()

        context['user_post']=user_post
        context['comment']=all_cmt

        return context

#--------------------------------------------------------------------------
class post_detail(generic.DetailView):
    model = UserPost
    template_name = 'post/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ** in this kwargs, single user query is present 
        user_post = kwargs['object']
        all_cmt = UserComments.objects.all().order_by('-created_at')
        user_post.is_liked = Like.objects.filter(user=self.request.user,post=kwargs['object']).exists()
    
        context['post'] = user_post
        context['comment'] = all_cmt

        return context
    
#--------------------------------------------------------------------------

class comment_on_post(generic.FormView):
    form_class = UserCommentForm    
    def form_valid(self,form):
        return super().form_valid(form)
    
    def post(self,request,pk,*args, **kwargs):
        comment_text = self.request.POST.get('comment')
        if not comment_text:
            return JsonResponse({'success': False, 'message': 'Please add comment...'})
        post = UserPost.objects.get(id=pk)
        new_comment = UserComments.objects.create(user=self.request.user, post=post, comment=comment_text)
        new_comment.save()
        return JsonResponse({'success': True})
        
class update_on_comment(generic.View):
    def post(self,request):
        comment_text = self.request.POST.get('comment')
        if not comment_text:
            return JsonResponse({'success': False, 'message': 'Please add comment...'})
        
        cmt = UserComments.objects.get(id=self.request.POST.get('cmt_id'))
        cmt.comment = comment_text
        cmt.save()
        return JsonResponse({'success': True})
        

class delete_comment(generic.View):
    def get(self,request):
        cmt_id = self.request.GET.get('cmt_id')
        UserComments.objects.get(id=cmt_id).delete()
        return JsonResponse({'success': True})
    

class like(generic.View):
    def get(self,request,pk):
        user = request.user
        post = get_object_or_404(UserPost,id=pk)
        #checking post is liked or not by cur user
        like = Like.objects.filter(user=user,post=post)
    
        if liked:= like.count():
            post.like = post.like - 1
            post.save()
            like.delete()
        else:
            like = Like.objects.create(user=user,post=post)
            like.save()
            post.like = post.like + 1
            post.save()
        
        return JsonResponse({'success': True})
