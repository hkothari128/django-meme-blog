from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author','content', 'post',)
        
        # widgets = {
        #     'author': forms.HiddenInput(),
        #     'post': forms.HiddenInput(),
        #     'date_commented': forms.HiddenInput()
        # }