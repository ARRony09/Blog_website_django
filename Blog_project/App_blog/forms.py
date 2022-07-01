from dataclasses import field
from pyexpat import model
from django import forms
from App_blog.models import Blog,Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('comment',)