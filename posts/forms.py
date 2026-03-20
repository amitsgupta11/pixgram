from django import forms
from .models import Post, Comment, Story


class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = ['caption', 'image']
        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 4,
                'placeholder': "What's on your mind?",
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control', 'accept': 'image/*',
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model   = Comment
        fields  = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a comment…',
                'autocomplete': 'off',
            }),
        }
        labels = {'text': ''}


class StoryForm(forms.ModelForm):
    class Meta:
        model  = Story
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control', 'accept': 'image/*',
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add a caption (optional)',
            }),
        }
        labels = {
            'image':   'Story Photo',
            'caption': 'Caption (optional)',
        }