from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from post.models import *
from post.serializers import * 
from register.serializers import *


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    

class LikeAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,pk):
        user = self.request.user
        post = get_object_or_404(UserPost, id=pk)
        
        # Checking if the post is liked or not by the current user
        like = Like.objects.filter(user=user,post=post)
    
        if liked:= like.count():
            post.like = post.like - 1
            post.save()
            like.delete()
            return JsonResponse({'success': 'unlike post success'},status = status.HTTP_202_ACCEPTED)
        else:
            like = Like.objects.create(user=user,post=post)
            like.save()
            post.like = post.like + 1
            post.save()
            return JsonResponse({'success': "liked post success"},status = status.HTTP_201_CREATED)
        
    
class PostCreateAPIView(generics.CreateAPIView):
    queryset = UserPost.objects.all()
    serializer_class = PostSerializer

    
class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPost.objects.all()
    serializer_class = PostRetrieveUpdateDestroySerializer

class AllPostAPIView(generics.ListAPIView):
    queryset = UserPost.objects.all()
    serializer_class = AllPostSerializer

class CommentsAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    def get_queryset(self):
        post_id = self.kwargs.get('post_id')  #passing post_id in the URL
        return UserComments.objects.filter(post_id=post_id)
    
    
    
####Register api#################################################

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

# class RegisterListCreateAPIView(generics.ListCreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = RegisterSerializer

# class RegisterRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = RegisterSerializer
#----------------------------------------------------------------
#login
class LoginApiView(generics.views.APIView):
    def post(self,request):
        serializer = LoginApiSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user= authenticate(username=username, password=password)
            token = get_tokens_for_user(user)
            if user:
                login(request,user)
                return Response({'token':token,'msg':'login success'},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'login failed'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg':'user not logged in'},status=status.HTTP_404_NOT_FOUND)

class LogoutApiView(generics.views.APIView):
    def get(self,request):
        logout(request)
        return Response({'msg':'Logout successfull'},status=status.HTTP_200_OK)
    
class ProfileApiView(generics.views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializers = ProfileSerializer(request.user)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
class PasswordChangeApiView(generics.views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data,context={'user': request.user})
        print(serializer)
        if serializer.is_valid():
            return Response({'msg': 'Password change successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)