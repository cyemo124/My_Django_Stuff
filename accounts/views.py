from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms
from django.contrib import messages
from django.contrib.auth.views import LoginView

# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

class CustomLoginView(LoginView):
    def form_invalid(self, form):
        # Call super to get the default form_invalid behavior
        response = super().form_invalid(form)

        # Check if the user exists before attempting to authenticate
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(self.request, 'User does not exist or invalid credentials.')
        else:
            messages.error(self.request, 'Invalid credentials. Please try again.')

        return response
