from django import forms
from .models import ForumThread, Post
from django.utils.text import slugify

class ThreadForm(forms.ModelForm):
    class Meta:
        model = ForumThread
        fields = ['title', 'slug', 'description']

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if not slug:
            slug = slugify(self.cleaned_data.get('title', ''))
        return slug

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data['content'].strip()
        if len(content) < 5:
            raise forms.ValidationError("Повідомлення занадто коротке.")
        return content
