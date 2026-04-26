from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': "What's on your mind?",
            'rows': 3,
            'class': 'form-control',
        }),
        max_length=2000,
    )

    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Write a comment...',
            'rows': 2,
            'class': 'form-control',
        }),
        max_length=500,
    )

    class Meta:
        model = Comment
        fields = ['content']