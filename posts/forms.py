from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'body')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mt-2', 'placeholder': 'Title'}),
            'category': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'body': forms.Textarea(attrs={'class': 'form-control mt-2', 'placeholder': 'Content'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        return new_slug


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(
        attrs={'class': 'form-control mt-2', 'placeholder': 'Name'}))
    email_to = forms.EmailField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control mt-2', 'placeholder': 'Email To'}))
    email_from = forms.EmailField(max_length=50, widget=forms.TextInput(
        attrs={'class': 'form-control mt-2', 'placeholder': 'Email From'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'class': 'form-control mt-2', 'placeholder': 'Type Your Comment here...'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control mt-2', 'placeholder': 'Type your comment here...'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Type to Search...'}
    ))
