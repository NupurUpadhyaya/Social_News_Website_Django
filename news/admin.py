from django.contrib import admin
from .models import Story, Comment, Tag, UserProfile

# Register your models here.

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'score')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'body_text', 'url')
    raw_id_fields = ('author',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'story', 'created_at', 'score')
    list_filter = ('created_at',)
    search_fields = ('text',)
    raw_id_fields = ('author', 'story', 'parent')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'karma')
    search_fields = ('user__username',)
