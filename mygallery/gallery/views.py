from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Picture, Like
from .forms import RegisterForm

def home(request):
    pictures = Picture.objects.all()
    return render(request, 'gallery/home.html', {'pictures': pictures})

def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(user=request.user, picture=picture).exists()
    return render(request, 'gallery/picture_detail.html', {
        'picture': picture,
        'liked': liked
    })

@login_required
def liked_pictures(request):
    likes = Like.objects.filter(user=request.user)
    pictures = [like.picture for like in likes]
    return render(request, 'gallery/liked.html', {'pictures': pictures})

@login_required
def like_picture(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, picture=picture)
    if not created:
        like.delete()
    return redirect('picture-detail', pk=pk)

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Registration error")
    else:
        form = RegisterForm()
    return render(request, 'gallery/register.html', {'form': form})