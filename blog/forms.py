from django import forms
from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title','image','content']

    def clean_title(self):
        title = self.cleaned_data.get('title')

        if title.isdigit():
            raise forms.ValidationError('The title cannot only consist of numbers')

        if len(title) <= 3:
            raise forms.ValidationError('Title cannot be less than 3 characters')

        return title
    
    def clean_content(self):
        content = self.cleaned_data.get('content')

        if content.isdigit():
            raise forms.ValidationError('The content cannot only consist of numbers')

        if len(content) <= 3:
            raise forms.ValidationError('Content cannot be less than 3 characters')

        return content

