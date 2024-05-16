from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, Http404
from django.views import generic
from .forms import UserPostForm, UserCommentForm
from .models import *
from django.conf import settings
# from django.views.decorators.cache import cache_page
#--------------------------------------------------------------------------
import requests, os
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
from post.tasks import send_email_task

Email_Api_Key = "AIzaSyDi5Ta4oJtbiBeycRVdGeRcLrxLQhh7atE"
#sending mail
# Abstract Api

def validate_email(email):
    response = requests.get("https://emailvalidation.abstractapi.com/v1/?api_key=371b6bc2168b46838526cbf0eae84649&email=luhulu329@gmail.com")
    data = response.json()
    valueText = data.get('is_valid_format')
    # is_valid_format and is_mx_found and is_smtp_valid and not is_catchall_email and not is_role_email and not is_free_email
    return valueText.get('value')

def send_email(subject, from_email, to_email, reply_to, attachments=None, context=None):
    # if validate_email(to_email) and validate_email(reply_to):
    # Ensure context is a dictionary
    if context is None:
        context = {}

    
    # context is passed for email in html_message
    html_message = render_to_string('post/email.html', context=context)
    plain_message = strip_tags(html_message)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=from_email,
        to=[to_email],
        reply_to=[reply_to],

    )
    email.attach_alternative(html_message, "text/html")
    if attachments is not None:
        img_path = f'{settings.BASE_DIR}/media/user_post/{str(attachments)}'
        with open(img_path, 'rb') as file:
            image_data = file.read()
            banner_image = MIMEImage(image_data)
            # banner_image.add_header('Content-ID', '<image>')
            email.attach(banner_image)
    
    email.send()
    print('Your email has been sent successfully.')
    # else:
    #     print("Invalid recipient email address.")



#------Custom single-----------------
from django.dispatch import Signal, receiver
import datetime

hello_signal = Signal()

@receiver(hello_signal)
def my_signal(sender,instance, **kwargs):
    message = kwargs.get("message")
    current_time = datetime.datetime.now()
    with open("logdata.txt", "a") as file:
        file.write(str(current_time) + "\t" + instance.user.username + " " + message + "\n")


# hello_signal.send(sender=None,instance=UserPost.objects.all().first(), message="Custom Signal form Post view's : Hello, u r logged in")
#---------------------------------------------------------

class PostFormView(generic.FormView):
    form_class = UserPostForm
    template_name = 'post/post.html'
    success_url = '/post/view_post/'

    # when request.POST then    
    def form_valid(self,form):
        user_post = form.save(commit=False)
        user_post.user = self.request.user            
        user_post.save()
    #---Celery--email----------
        context = {
            'full_name': f"{self.request.user.first_name} {self.request.user.last_name}"
        }
        html_message = render_to_string('post/email.html', context=context)
        plain_message = strip_tags(html_message)
        # send_email_task.delay(plain_message,html_message)
        task_id = "a1"
        send_email_task.apply_async(kwargs={"plain_message": plain_message, "html_message": html_message})
    #--------------Email-----------------------------------------------------------------
        subject = "Post Saved"
        headers = {"My-Header": "hello i am header"}
        from_email = settings.EMAIL_HOST_USER

        to_email = "ajayparihar876@gmail.com"
        attachments = form.cleaned_data['image']        
        reply_to = 'ajayparihar876@gmail.com'
        
        # send_email(subject=subject,from_email= from_email,to_email= to_email,reply_to=reply_to,attachments=None,context=context)
    #------------------------------------------------------------------------------------

        hello_signal.send(sender=None,instance=UserPost.objects.all().first(), message="Custom Signal form Post view's : Post saved")

        return super().form_valid(form)
    
    

#-------------------------------------------------------------------------------------
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

    # paggination
    # https://testdriven.io/blog/django-pagination/
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

        page_num = self.request.GET.get('page', 1)
        paginator = Paginator(user_post, 1) # 6 employees per page

        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            # if page is not an integer, deliver the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if the page is out of range, deliver the last page
            page_obj = paginator.page(paginator.num_pages)


        context['user_post'] = page_obj
        context['comment'] = all_cmt

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
        cmt_id = self.request.POST.get('cmt_id')
        cmt = get_object_or_404(UserComments,id=cmt_id)
        if not cmt:
            return Http404
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
        print('user liked')
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
