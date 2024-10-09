from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label='Your age', min_value=0, max_value=100)
    bio = forms.CharField(label='Biography', widget=forms.Textarea)

def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and 'virus' in file.name:
        raise ValidationError('Filename should not contain "virus"')

class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
