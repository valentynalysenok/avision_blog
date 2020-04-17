from django.db import models
from django.urls import reverse
from django.utils import timezone

from posts.utils import custom_slugify
from users.models import CustomUser


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = custom_slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('posts:update_post', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('posts:delete_post', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title
