from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserPostForm, UserCommentForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from register.models import CustomUser
from django.views import generic
#--------------------------------------------------------------------------

class PostFormView(generic.FormView):
    form_class = UserPostForm
    template_name = 'post/post.html'
    success_url = '/post/view_post/'

    # when request.POST then    
    def form_valid(self,form):
        user_post = form.save(commit=False)
        user_post.user = self.request.user            
        user_post.save()
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
    
    def post(self,request,post_id,*args, **kwargs):
        comment_text = self.request.POST.get('comment')
        if not comment_text:
            return JsonResponse({'success': False, 'message': 'Please add comment...'})
        post = UserPost.objects.get(id=post_id)
        new_comment = UserComments.objects.create(user=request.user, post=post, comment=comment_text)
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
            
        