from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)  # Add an ImageField to the form

    class Meta:
        model = Post
        fields = ['message', 'image']  # Exclude the 'group' field from the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial value for the message field to an empty string
        self.fields['message'].initial = ''
