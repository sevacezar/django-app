from typing import Any

from django.contrib.auth.models import User, Group, Permission
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        user = User.objects.get(pk=2)
        group, created = Group.objects.get_or_create(
            name='profile_manager',
        )  # creation new group
        permission_profile = Permission.objects.get(
            codename='view_profile',
        )  # creation new permission
        permission_logentry = Permission.objects.get(
            codename='view_logentry',
        )

        group.permissions.add(permission_profile)  # adding permission to group
        user.groups.add(group)  # adding user to group
        user.user_permissions.add(permission_logentry)  # adding permisiion to user 

        group.save()
        user.save()