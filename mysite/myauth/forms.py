from django import forms
from django.forms import ClearableFileInput

from .models import Profile


class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        