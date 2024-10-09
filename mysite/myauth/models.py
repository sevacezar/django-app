from django.contrib.auth.models import User
from django.db import models


def profile_avatars_directory_path(instance: 'Profile', filename: str):
    return 'profiles/profile_{pk}/images/{filename}'.format(
        pk=instance.user.pk,
        filename=filename,
    )

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=False, blank=True, upload_to=profile_avatars_directory_path)

