from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.email
