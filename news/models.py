from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Story(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True)
    body_text = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    tags = models.ManyToManyField(Tag, related_name='stories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User, related_name='upvoted_stories', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-score', '-created_at']
        verbose_name_plural = 'stories'

    def clean(self):
        if not self.url and not self.body_text:
            raise ValidationError('Either URL or body text must be provided')

class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.IntegerField(default=0)
    upvoted_by = models.ManyToManyField(User, related_name='upvoted_comments', blank=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.story.title}'

    class Meta:
        ordering = ['-score', 'created_at']

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    karma = models.IntegerField(default=0)

    def __str__(self):
        return f'Profile for {self.user.username}'
