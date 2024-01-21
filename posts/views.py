from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from django.contrib import messages

from . import models
from .models import Post
from . import forms
from .forms import PostForm
from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user','group')

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
        
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context
    

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))
    

class CreateRegularPost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    form_class = PostForm  # Use the form for regular posts
    model = Post
    template_name = 'posts/post_form.html'  # Update with your actual template name for regular posts

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        # Check if an image file was uploaded
        if 'image' in self.request.FILES:
            self.object.image = self.request.FILES['image']  # Assign the uploaded image to the Post model field
        
        # Save the Post object with the uploaded image
        self.object.save()

        messages.success(self.request, 'Regular post created successfully.')
        return redirect('posts:single', username=self.request.user.username, pk=self.object.pk)

    # Other methods as needed

class CreatePost(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    model = Post
    template_name = 'posts/group_post_form.html'  # Update with your actual template name

    def form_valid(self, form):
        group_id = self.request.POST.get('group')
        group = get_object_or_404(Group, id=group_id)

        if self.request.user in group.members.all():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.group = group

            # Handle the image upload
            if 'image' in self.request.FILES:
                self.object.image = self.request.FILES['image']

            self.object.save()

            messages.success(self.request, 'Post created successfully.')
            return redirect('posts:single', username=self.request.user.username, pk=self.object.pk)
        else:
            form.add_error(None, 'You are not a member of this group. Cannot create a post.')
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()  # Provide groups to the template
        return context

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):

    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)
    
    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)