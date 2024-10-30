# file_management/models.py

from django.db import models
from django.conf import settings
from folder_management.models import Folder
import os

def user_directory_path(instance, filename):
    path = f'server/{instance.owner.username}'
    folder = instance.parent_folder

    folder_path_parts = []
    while folder:
        folder_path_parts.insert(0, folder.name)
        folder = folder.parent

    if folder_path_parts:
        folder_path = '/'.join(folder_path_parts)
        path = f'{path}/{folder_path}'

    return f'{path}/{filename}'

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=user_directory_path)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    size = models.PositiveIntegerField()
    extension = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
