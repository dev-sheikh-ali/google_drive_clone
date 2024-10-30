from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Folder
from django.http import JsonResponse
from file_management.models import File

@login_required
def list_folders(request, parent_id=None):
    """
    List folders and files under a given parent folder. If no parent_id is provided, list root folders and files.
    """
    parent_folder = None
    if parent_id:
        parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user)

    # Get subfolders of the current folder (or root folders if no parent_folder)
    folders = Folder.objects.filter(owner=request.user, parent=parent_folder)
    files = File.objects.filter(owner=request.user, parent_folder=parent_folder)  # Fetch files in the current folder

    print("Folders count:", folders.count())  # For debugging in console
    print("Files count:", files.count())  # For debugging in console

    # Collect ancestors for breadcrumb navigation
    breadcrumbs = []
    current = parent_folder
    while current is not None:
        breadcrumbs.insert(0, current)
        current = current.parent

    context = {
        'folders': folders,
        'files': files,  # Pass files to template
        'parent_folder': parent_folder,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'folder_management/list_folders.html', context)

@login_required
def create_folder(request, parent_id=None):
    if request.method == 'POST':
        name = request.POST.get('name')
        parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user) if parent_id else None

        # Check if a folder with the same name exists and append numbers if needed
        original_name = name
        counter = 1
        while Folder.objects.filter(name=name, owner=request.user, parent=parent_folder).exists():
            name = f"{original_name} ({counter})"
            counter += 1

        folder = Folder(name=name, owner=request.user, parent=parent_folder)
        folder.save()
        messages.success(request, "Folder created successfully!")

        if parent_folder:
            return redirect('list_folders_nested', parent_id=parent_folder.id)
        return redirect('list_folders')

    if parent_id:
        return redirect('list_folders_nested', parent_id=parent_id)
    return redirect('list_folders')

@login_required
def create_subfolder(request, parent_id):
    """
    Create a subfolder within the specified parent folder.
    """
    parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')

        # Check if a folder with the same name exists and append numbers if needed
        original_name = name
        counter = 1
        while Folder.objects.filter(name=name, owner=request.user, parent=parent_folder).exists():
            name = f"{original_name} ({counter})"
            counter += 1

        subfolder = Folder(name=name, owner=request.user, parent=parent_folder)
        subfolder.save()
        messages.success(request, "Subfolder created successfully!")

        return redirect('list_folders_nested', parent_id=parent_folder.id)

    return redirect('list_folders_nested', parent_id=parent_folder.id)

@login_required
def update_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    if request.method == 'POST':
        folder.name = request.POST.get('name')

        # Check if another folder with the same name exists under the same parent
        existing_folder = Folder.objects.filter(
            owner=request.user, 
            parent=folder.parent, 
            name=folder.name
        ).exclude(id=folder.id)

        if existing_folder.exists():
            # Append numbers to folder name if there's a conflict
            original_name = folder.name
            counter = 1
            while Folder.objects.filter(name=folder.name, owner=request.user, parent=folder.parent).exclude(id=folder.id).exists():
                folder.name = f"{original_name} ({counter})"
                counter += 1

        folder.save()
        messages.success(request, "Folder updated successfully!")

        # Redirect to the correct parent folder or root
        if folder.parent:
            return redirect('list_folders_nested', parent_id=folder.parent.id)
        return redirect('list_folders')

    # Redirect to the correct parent folder or root if GET request
    if folder.parent:
        return redirect('list_folders_nested', parent_id=folder.parent.id)
    return redirect('list_folders')

@login_required
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    if request.method == 'POST':
        parent_id = folder.parent.id if folder.parent else None
        folder.delete()
        messages.success(request, "Folder deleted successfully!")

        if parent_id:
            return redirect('list_folders_nested', parent_id=parent_id)
        return redirect('list_folders')
    return redirect('list_folders', parent_id=folder.parent.id if folder.parent else None)

@login_required
def move_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)

    if request.method == 'POST':
        new_parent_id = request.POST.get('new_parent_id')
        if new_parent_id:
            new_parent = get_object_or_404(Folder, id=new_parent_id, owner=request.user)

            # Ensure the selected new parent is not a descendant of the folder being moved
            if not is_child_folder(folder, new_parent):
                # Check for duplicate names and append numbers if needed
                original_name = folder.name
                counter = 1
                name = original_name
                while Folder.objects.filter(name=name, owner=request.user, parent=new_parent).exists():
                    name = f"{original_name} ({counter})"
                    counter += 1
                folder.name = name
                folder.parent = new_parent
                folder.save()
                messages.success(request, "Folder moved successfully!")
            else:
                messages.error(request, "Invalid operation. Cannot move a folder into its own child or itself.")

        return redirect('list_folders_nested', parent_id=new_parent_id)

    # Retrieve all folders owned by the user except for the current folder and its descendants
    all_folders = Folder.objects.filter(owner=request.user).exclude(id=folder.id)
    valid_folders = [f for f in all_folders if not is_child_folder(folder, f)]

    return render(request, 'folder_management/move_folder_modal.html', {
        'folder': folder,
        'all_folders': valid_folders,
    })


@login_required
def copy_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    if request.method == 'POST':
        new_parent_id = request.POST.get('new_parent_id')
        if new_parent_id:
            new_parent = get_object_or_404(Folder, id=new_parent_id, owner=request.user)
            if not is_child_folder(folder, new_parent):
                # Check for duplicate names and append numbers if needed
                original_name = f"{folder.name} - Copy"
                counter = 1
                name = original_name
                while Folder.objects.filter(name=name, owner=request.user, parent=new_parent).exists():
                    name = f"{original_name} ({counter})"
                    counter += 1
                copied_folder = Folder(name=name, parent=new_parent, owner=request.user)
                copied_folder.save()
                messages.success(request, "Folder copied successfully!")
            else:
                messages.error(request, "Invalid copy operation. You cannot copy a folder into its child.")
        else:
            original_name = f"{folder.name} - Copy"
            counter = 1
            name = original_name
            while Folder.objects.filter(name=name, owner=request.user, parent=None).exists():
                name = f"{original_name} ({counter})"
                counter += 1
            copied_folder = Folder(name=name, owner=request.user)
            copied_folder.save()
            messages.success(request, "Folder copied to the root successfully!")

        return redirect('list_folders_nested', parent_id=new_parent_id if new_parent_id else None)

    all_folders = Folder.objects.filter(owner=request.user).exclude(id=folder.id)
    return render(request, 'folder_management/copy_folder.html', {'folder': folder, 'all_folders': all_folders})

# Helper function to check if new_parent is a child of folder
def is_child_folder(folder, new_parent):
    """Checks if the new parent is a child of the given folder."""
    current = new_parent
    while current:
        if current == folder:
            return True
        current = current.parent
    return False
