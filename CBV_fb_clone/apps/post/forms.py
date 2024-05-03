from django import forms

from .models import UserPost, UserComments


class UserPostForm(forms.ModelForm):

    class Meta:
        model = UserPost
        fields = ['image', 'cap', 'desc', 'location']
        widgets = {}

    def clean(self):
        cleaned_data = super().clean()
        cap = cleaned_data.get("cap")
        location = cleaned_data.get("location")

        if not cap:
            self.add_error('cap', 'This field is required.')

        if not location:
            self.add_error('location', 'This field is required.')

        return cleaned_data

class UserCommentForm(forms.ModelForm):
    class Meta:
        model = UserComments
        fields = ['comment']

