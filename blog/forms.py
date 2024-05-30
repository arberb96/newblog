# from django import forms 
# from .models import Post, Paragraph
# from django.forms import inlineformset_factory

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ["title", "title_tag"]
        
#         # fields = ["title", "title_tag", "body"]
        
#         # widgets = {
#         #     "title": forms.TextInput(attrs={"class": "form-control"}),
#         #     "title_tag": forms.TextInput(attrs={"class": "form-control"}),
#         #     "body": forms.Textarea(attrs={"class": "form-control"}),
#         # }
        
# ParagraphFormSet = inlineformset_factory(Post, Paragraph, fields=('title', 'image', 'text'), extra=1, can_delete=True)

from django import forms
from django.forms import inlineformset_factory
from .models import Post, Paragraph

from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image']

class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = ['title', "image", "text"]

# Ensure 'extra=1' for one empty form initially, and 'can_delete=False' since deletion isn't a feature you mentioned needing.
ParagraphFormSet = inlineformset_factory(Post, Paragraph, form=ParagraphForm, extra=1, can_delete=True, can_delete_extra=False)
# This creates a formset for paragraphs linked to a post
# ParagraphFormSet = inlineformset_factory(Post, Paragraph, form=ParagraphForm, extra=1, can_delete=False)