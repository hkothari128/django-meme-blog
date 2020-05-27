from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author','content', 'post',)
        
        widgets = {
            'content': forms.Textarea(attrs={'rows':0, 'cols':0}),
        }