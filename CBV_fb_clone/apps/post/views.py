from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserPostForm, UserCommentForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count
from register.models import CustomUser
from django.views import generic
#--------------------------------------------------------------------------

class PostFormView(generic.View):
    form_class = UserPostForm
    template_name = 'post/post.html'
    
    def get(self,request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})
    
    def post(self,request):
        form = UserPostForm(request.POST, request.FILES)
        if form.is_valid():
            user_post = form.save(commit=False)
            user_post.user = request.user            
            user_post.save()
            return redirect('Post:view_post')  # Redirect to dashboard upon successful post creation
#--------------------------------------------------------------------------

class dashboard(generic.TemplateView):
    template_name = 'post/dashboard.html'

#--------------------------------------------------------------------------
class update_post(generic.View):
    def get(self,request,id):
        fm = UserPostForm()
        return render(request, 'post/post.html', {'form': fm})

    def post(self,request,id):
        # new_obj1 = get_object_or_404(UserPost,id = pk)
        new_obj1 = UserPost.objects.get(id = id)
        new_obj1.image = request.POST.get('image')
        
        fm = UserPostForm(request.POST, request.FILES, instance=new_obj1)
        if fm.is_valid():
            fm.save()
        return redirect('Post:dashboard')  # Redirect to dashboard upon successful post creation
    

#--------------------------------------------------------------------------
class delete_post(generic.View):
    def get(self,request,id):
        user_post = UserPost.objects.get(id = id)
        user_post.delete()
        return redirect('/post/view_post/')

#--------------------------------------------------------------------------
class all_user_post(generic.View):
    def get(self,request):
        all_post = UserPost.objects.all().order_by('-created_at')
        for post in all_post:
            post.is_liked = Like.objects.filter(user=request.user,post=post).exists()
        all_cmt = UserComments.objects.all().order_by('-created_at')
        return render(request,'post/all_user_post.html',{'all_user_post':all_post,'comment':all_cmt})
        

#--------------------------------------------------------------------------
class view_post(generic.View):
    def get(self,request):
        user_post = UserPost.objects.filter(user=request.user).order_by('-created_at')
        all_cmt = UserComments.objects.all().order_by('-created_at')
        for post in user_post:
            post.is_liked = Like.objects.filter(user=request.user,post=post).exists()
        return render(request, 'post/profile.html',{'user_post':user_post,'comment':all_cmt})


#--------------------------------------------------------------------------
class post_detail(generic.View):
    def get(self,request,post_id,*args, **kwargs):
        user_post = UserPost.objects.get(id = post_id)
        all_cmt = UserComments.objects.all().order_by('-created_at')
        user_post.is_liked = Like.objects.filter(user=request.user,post=user_post).exists()
        return render(request,'post/post_detail.html',{'post':user_post,'comment':all_cmt})
#--------------------------------------------------------------------------
class comment_on_post(generic.View):
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
    def get(self,request,pk,*args, **kwargs):
        user = request.user
        post = UserPost.objects.get(id = pk)

        liked = Like.objects.filter(user=user,post=post).count()
        if not liked :
            like = Like.objects.create(user=user,post=post)
            like.save()
            post.like = post.like + 1
            post.save()
            return JsonResponse({'success': True})

class unlike(generic.View):
    def get(self,request,pk,*args, **kwargs):
        user = request.user
        post = UserPost.objects.get(id = pk)
        like = Like.objects.filter(user=user,post=post)
    
        if liked:= like.count():
            post.like = post.like - 1
            post.save()
            like.delete()
        return JsonResponse({'success': True})
