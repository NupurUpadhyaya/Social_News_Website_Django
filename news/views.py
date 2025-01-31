from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Story, Comment, Tag
from .forms import StoryForm, CommentForm, UserRegistrationForm

def home(request):
    stories = Story.objects.all()
    tag = request.GET.get('tag')
    if tag:
        stories = stories.filter(tags__name=tag)
    
    paginator = Paginator(stories, 20)
    page = request.GET.get('page')
    stories = paginator.get_page(page)
    
    return render(request, 'news/home.html', {'stories': stories})

def story_detail(request, pk):
    story = get_object_or_404(Story, pk=pk)
    comments = Comment.objects.filter(story=story, parent=None)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.story = story
            comment.author = request.user
            comment.save()
            return redirect('story_detail', pk=pk)
    else:
        form = CommentForm()
    
    return render(request, 'news/story_detail.html', {
        'story': story,
        'comments': comments,
        'form': form
    })

@login_required
def submit_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            form.save_m2m()  # Save tags
            return redirect('home')
    else:
        form = StoryForm()
    return render(request, 'news/submit_story.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'news/register.html', {'form': form})

@login_required
def vote(request, pk, vote_type):
    if vote_type == 'story':
        item = get_object_or_404(Story, pk=pk)
    else:
        item = get_object_or_404(Comment, pk=pk)
    
    if request.user in item.upvoted_by.all():
        # Remove upvote
        item.score -= 1
        item.upvoted_by.remove(request.user)
        item.save()
    else:
        # Add upvote
        item.score += 1
        item.upvoted_by.add(request.user)
        item.save()
    
    # Return to the previous page
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            comment = Comment.objects.create(
                story=parent_comment.story,
                author=request.user,
                parent=parent_comment,
                text=text
            )
            return redirect('story_detail', pk=parent_comment.story.pk)
    return redirect('story_detail', pk=parent_comment.story.pk)

def tag_stories(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    stories = Story.objects.filter(tags=tag).order_by('-score', '-created_at')
    
    paginator = Paginator(stories, 20)  # Show 20 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/home.html', {
        'stories': page_obj,
        'current_tag': tag,
    })

def search(request):
    query = request.GET.get('q')
    sort = request.GET.get('sort', '-score')
    
    if query:
        stories = Story.objects.filter(
            Q(title__icontains=query) |
            Q(body_text__icontains=query) |
            Q(url__icontains=query) |
            Q(comments__text__icontains=query)
        ).distinct()
        
        if sort == '-score':
            stories = stories.order_by('-score')
        elif sort == 'score':
            stories = stories.order_by('score')
        elif sort == '-date':
            stories = stories.order_by('-created_at')
        elif sort == 'date':
            stories = stories.order_by('created_at')
    else:
        stories = Story.objects.none()
    
    return render(request, 'news/search.html', {
        'stories': stories,
        'query': query,
        'sort': sort
    })
