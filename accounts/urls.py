from django.urls import path
from . import views

urlpatterns = [
    path('front/', views.front_view, name='front'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('posts/', views.posts_view, name='posts'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('posts/delete/<int:post_id>/', views.delete_post_view, name='delete_post'),
]
