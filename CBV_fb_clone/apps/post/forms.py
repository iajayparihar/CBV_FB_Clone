from django import forms

from .models import UserPost, UserComments


class UserPostForm(forms.ModelForm):

    class Meta:

        model = UserPost

        fields = ['image','cap','desc','location']
        widgets = {}



class UserCommentForm(forms.ModelForm):

    class Meta:

        model = UserComments

        fields = ['comment']