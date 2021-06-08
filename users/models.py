from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    follow = models.ManyToManyField(
        'self', blank=True, symmetrical=False, related_name='follower',
    )
