from django import forms
from .models import Post  # Import your Post model

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', 'image']  # Adjust fields as per your Post model

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can customize form fields here if needed
        # For instance, setting attributes or initial values
