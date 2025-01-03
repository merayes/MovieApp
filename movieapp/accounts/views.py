from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Giriş sayfasına yönlendirme
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})
