from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']

# ProfileUpdateForm olarak da aynı formu kullanabilirsiniz
class ProfileUpdateForm(ProfileForm):
    pass