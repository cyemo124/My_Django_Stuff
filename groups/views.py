from typing import Any
from django.shortcuts import render, redirect
from django.contrib import messages
from . import models

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404

from groups.models import Group,GroupMember

from django.db.utils import IntegrityError

from .forms import PostForm
from posts.models import Post



class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group
    template_name = 'groups/group_detail.html'  # Update with your actual template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the posts related to the current group
        context['post_list'] = self.object.group_posts.all()

        return context

class ListGroup(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'Warning already a member!')
        else:
            messages.success(self.request,'You are now a member!')

        return super().get(request,*args,**kwargs)
        


class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self,request,*args,**kwargs):

        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'Sorry you are not in this group!')
        else:
            membership.delete()
            messages.success(self.request,'You have left the group!')
        return super().get(request,*args,**kwargs)
    
class CreatePost(LoginRequiredMixin, generic.CreateView):
    form_class = PostForm
    model = Post
    template_name = 'groups/group_detail.html'  # Update with your actual template name

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
    
    