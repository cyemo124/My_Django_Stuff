from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Group, Permission

# Create your models here.

class User(AbstractUser, PermissionsMixin):

    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_set'
    )

    def __str__(self):
        return "@{}".format(self.username)
