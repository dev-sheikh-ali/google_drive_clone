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
        'all_folders': Folder.objects.filter(owner=request.user),  # Pass all folders for modal
    }
    return render(request, 'file_management/list_files.html', context) 

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

        if folder.parent:
            return redirect('list_folders_nested', parent_id=folder.parent.id)
        return redirect('list_folders')

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
                # Move the folder
                folder.parent = new_parent
                folder.save()
                
                # Move all files in the original folder to the new parent
                files_to_move = File.objects.filter(parent_folder=folder)
                for file in files_to_move:
                    file.parent_folder = None  # If you want to set the parent folder to the new folder, set it as follows:
                    file.parent_folder = new_parent  # Update this line to move the files to the new parent folder
                    file.save()

                messages.success(request, "Folder and its contents moved successfully!")
            else:
                messages.error(request, "Invalid operation. Cannot move a folder into its own child or itself.")

        return redirect('list_folders_nested', parent_id=new_parent_id)

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
                original_name = folder.name
                counter = 1
                name = original_name
                while Folder.objects.filter(name=name, owner=request.user, parent=new_parent).exists():
                    name = f"{original_name} ({counter})"
                    counter += 1
                
                # Create a copy of the folder
                copied_folder = Folder(name=name, owner=request.user, parent=new_parent)
                copied_folder.save()
                
                # Copy all files in the original folder
                files_to_copy = File.objects.filter(parent_folder=folder)
                for file in files_to_copy:
                    file_copy = File(
                        name=file.name,
                        file=file.file,  # This will create a new file in MEDIA_ROOT
                        owner=request.user,
                        parent_folder=copied_folder,
                        size=file.size,
                        extension=file.extension
                    )
                    file_copy.save()

                messages.success(request, "Folder copied successfully!")
            else:
                messages.error(request, "Invalid copy operation. You cannot copy a folder into its child.")

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
