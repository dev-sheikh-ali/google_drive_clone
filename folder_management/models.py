# folder_management/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_full_path(self):
        """Returns the full path of the folder as a string."""
        if self.parent:
            return f"{self.parent.get_full_path()} / {self.name}"
        return self.name

    def is_descendant(self, folder):
        """Returns True if the given folder is a descendant of this folder."""
        if self == folder:
            return True
        if self.parent:
            return self.parent.is_descendant(folder)
        return False

    def get_ancestors(self):
        """Returns a list of all ancestor folders, used for breadcrumbs."""
        ancestors = []
        current = self.parent
        while current:
            ancestors.insert(0, current)
            current = current.parent
        return ancestors
