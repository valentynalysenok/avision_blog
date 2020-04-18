from taggit.managers import TaggableManager

from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import CustomUser
from .utils import custom_slugify, send_email


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField()
    tags = TaggableManager()
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


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # post.comments.all()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')  # user.comments.all()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post}'

    def save(self, *args, **kwargs):
        if not self.id:
            send_email(f"Avision Blog - Comment was added to your post {self.post.title}",
                       f"Username: {self.user.username}\n"
                       f"Email: {self.user.email}\n"
                       f"Comment body: {self.body}",
                       (self.post.author.email,))
        super().save(*args, **kwargs)
