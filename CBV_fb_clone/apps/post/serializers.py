from rest_framework import serializers
from .models import *

class PostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    class Meta:
        model = UserPost
        fields = ['user', 'image', 'location', 'created_at', 'like', 'cap', 'desc']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = UserComments
        fields = '__all__'

class AllPostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True,read_only = True, source= 'post') # include all comments

    class Meta:
        model = UserPost
        fields = ["id", 'user', "image", 'location', 'created_at', 'like', 'cap', 'desc', "comments"]

class PostRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True, read_only=True,source='post')  # include all comments || source is related name of comments model post field
    class Meta:
        model = UserPost
        fields = ["id", 'user', "image", 'location', 'created_at', 'like', 'cap', 'desc', "comments"]
    