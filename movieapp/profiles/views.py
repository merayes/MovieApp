from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from .forms import ProfileUpdateForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'profiles/edit_profile.html', {'form': form})

def profile_view(request):
    """Kullanıcının kendi profilini görüntüler."""
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'profiles/profile_view.html', {'profile': profile})

def user_profile(request, username):
    """Belirli bir kullanıcının profilini görüntüler."""
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'profiles/user_profile.html', {'profile': profile})

