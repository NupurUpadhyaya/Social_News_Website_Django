from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Story, Comment

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        if ' ' in username:
            raise forms.ValidationError("Username cannot contain whitespace")
        return username

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'url', 'body_text', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'body_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['url'].required = False
        self.fields['body_text'].required = False
        self.fields['tags'].help_text = "Select one or more tags for your story"

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        body_text = cleaned_data.get('body_text')
        
        if not url and not body_text:
            raise forms.ValidationError("Either URL or body text must be provided")
        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4}),
        }
