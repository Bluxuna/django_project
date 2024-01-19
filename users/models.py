from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    avatar = models.TextField()
    bio = models.TextField()


class User(AbstractUser):
    height = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)



