# folder_management/templatetags/folder_tags.py
from django import template
from folder_management.models import Folder

register = template.Library()

@register.filter
def is_descendant(folder, potential_ancestor):
    """
    Custom template filter to check if 'folder' is a descendant of 'potential_ancestor'.
    """
    if not isinstance(folder, Folder) or not isinstance(potential_ancestor, Folder):
        return False

    current_folder = folder
    while current_folder.parent:
        if current_folder.parent == potential_ancestor:
            return True
        current_folder = current_folder.parent

    return False
