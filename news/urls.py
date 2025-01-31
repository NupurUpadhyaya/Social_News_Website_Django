from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.submit_story, name='submit_story'),
    path('story/<int:pk>/', views.story_detail, name='story_detail'),
    path('vote/<str:vote_type>/<int:pk>/', views.vote, name='vote'),
    path('comment/<int:comment_id>/reply/', views.reply_comment, name='reply_comment'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='news/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='news/password_change.html', success_url='/'), name='password_change'),
    path('tag/<str:tag_name>/', views.tag_stories, name='tag_stories'),
    path('search/', views.search, name='search'),
]
