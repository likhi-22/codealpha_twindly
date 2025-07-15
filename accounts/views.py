from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django import forms
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    user = request.user
    notifications = []
    recent_posts = []
    if user.is_authenticated:
        notifications = user.received_requests.filter(is_seen=False)
        # Get user's posts and friends' posts
        friends = user.friends.all()
        recent_posts = user.posts.order_by('-created_at')
        friends_posts = []
        for friend in friends:
            friends_posts.extend(friend.posts.all())
        # Combine and sort by created_at, limit to 10
        all_posts = list(recent_posts) + friends_posts
        all_posts = sorted(all_posts, key=lambda p: p.created_at, reverse=True)[:10]
    else:
        all_posts = []
    return render(request, 'home.html', {'notifications': notifications, 'user': user, 'recent_posts': all_posts})

def profile_view(request):
    from django.shortcuts import get_object_or_404
    user_id = request.GET.get('user_id')
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user
    posts = user.posts.order_by('-created_at')
    if request.method == 'POST' and user == request.user:
        bio = request.POST.get('bio', '')
        user.bio = bio
        if 'profile_photo' in request.FILES:
            user.profile_photo = request.FILES['profile_photo']
        user.save()
    return render(request, 'profile.html', {'user': user, 'posts': posts})

def search_view(request):
    query = request.GET.get('q', '')
    results = []
    message = ''
    if query:
        results = User.objects.filter(username__icontains=query).exclude(id=request.user.id)
    if request.method == 'POST':
        to_user_id = request.POST.get('to_user_id')
        from .models import FriendRequest
        to_user = User.objects.get(id=to_user_id)
        if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user, is_seen=False).exists():
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            message = 'Friend request sent!'
        else:
            message = 'Friend request already sent.'
    return render(request, 'search_results.html', {'results': results, 'query': query, 'message': message})

def posts_view(request):
    from .models import Post, Like, Comment, Notification
    from django.core.files.storage import FileSystemStorage
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        if 'like_post_id' in request.POST:
            post_id = request.POST.get('like_post_id')
            post = Post.objects.get(id=post_id)
            like, created = Like.objects.get_or_create(user=request.user, post=post)
            if created:
                # Create notification for like
                if post.user != request.user:
                    Notification.objects.create(user=post.user, from_user=request.user, notif_type='like', post=post)
            else:
                like.delete()  # Unlike if already liked
            return redirect('posts')
        elif 'comment_post_id' in request.POST:
            post_id = request.POST.get('comment_post_id')
            text = request.POST.get('comment_text')
            post = Post.objects.get(id=post_id)
            if text:
                comment = Comment.objects.create(user=request.user, post=post, text=text)
                # Create notification for comment
                if post.user != request.user:
                    Notification.objects.create(user=post.user, from_user=request.user, notif_type='comment', post=post, comment=comment)
            return redirect('posts')
        else:
            caption = request.POST.get('caption', '')
            image = request.FILES.get('image')
            post = Post(user=request.user, content=caption)
            if image:
                post.image = image
            post.save()
            return redirect('posts')
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts.html', {'posts': posts})

def notifications_view(request):
    from .models import FriendRequest, Notification
    if not request.user.is_authenticated:
        return redirect('login')
    requests = request.user.received_requests.filter(is_seen=False)
    notifications = Notification.objects.filter(user=request.user, is_seen=False).order_by('-created_at')
    if request.method == 'POST':
        req_id = request.POST.get('request_id')
        action = request.POST.get('action')
        friend_req = FriendRequest.objects.get(id=req_id, to_user=request.user)
        if action == 'accept':
            request.user.friends.add(friend_req.from_user)
            friend_req.from_user.friends.add(request.user)
        friend_req.is_seen = True
        friend_req.save()
        requests = request.user.received_requests.filter(is_seen=False)
    return render(request, 'notifications.html', {'requests': requests, 'notifications': notifications})

def front_view(request):
    return render(request, 'front.html')

def delete_post_view(request, post_id):
    from .models import Post
    from django.http import HttpResponseForbidden
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    if request.method == 'POST':
        post.delete()
        # Redirect to the page the user came from, fallback to posts
        next_url = request.POST.get('next', '/posts/')
        return redirect(next_url)
    # Optionally, render a confirmation page (not required if using modal)
    return redirect('/posts/')
