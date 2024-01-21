from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
import misaka 

from django.contrib.auth import get_user_model
User = get_user_model()

from django import template
register =  template.Library()


class Group(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(allow_unicode=True,unique=True)
    description = models.TextField(blank=True,default='')
    description_html = models.TextField(editable=False,default='',blank=True)
    members = models.ManyToManyField(User,through='GroupMember')
    posts = models.ManyToManyField('posts.Post', related_name='groups', blank=True)


    def __self__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})
    
    def member_count(self):
        return self.members.count()

    def post_count(self):
        return self.group_posts.count()
    
    class Meta:
        ordering = ['name']
    

class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name='membership', on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_username()
    
    class Meta:
        unique_together = ('group','user')
    pass
    

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Add an ImageField
    message_html = models.TextField(editable=False)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)

    def __str__(self):
        return self.message
    
    def save(self,*args,**kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.user.username,'pk':self.pk})
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']