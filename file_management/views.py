# file_management/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import File
from folder_management.models import Folder
from .forms import FileUploadForm
import os

MAX_FILE_SIZE = 40 * 1024 * 1024  # 40 MB
USER_MAX_STORAGE = 100 * 1024 * 1024  # 100 MB

@login_required
def upload_file(request, parent_id=None):
    parent_folder = None
    if parent_id:
        parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.parent_folder = parent_folder
            file.size = file.file.size
            file.extension = os.path.splitext(file.file.name)[1].lower()
            file.save()
            return JsonResponse({"message": "File uploaded successfully!", "file_name": file.name}, status=200)
        else:
            return JsonResponse({"error": "Invalid form submission"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)
@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    file_path = file.file.path
    if os.path.exists(file_path):
        os.remove(file_path)
    file.delete()
    messages.success(request, "File deleted successfully!")
    return redirect('list_folders', parent_id=file.parent_folder.id if file.parent_folder else None)

@login_required
def list_folders(request, parent_id=None):
    parent_folder = None
    if parent_id:
        parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user)

    # Fetch subfolders and files within the specified parent folder
    folders = Folder.objects.filter(owner=request.user, parent=parent_folder)
    files = File.objects.filter(owner=request.user, parent_folder=parent_folder)

    print("Folders count:", folders.count())
    print("Files count:", files.count())  # This will help you verify if files are being retrieved

    # Prepare breadcrumbs for navigation
    breadcrumbs = parent_folder.get_ancestors() if parent_folder else []

    context = {
        'folders': folders,
        'files': files,
        'parent_folder': parent_folder,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'folder_management/list_folders.html', context)

@login_required
def view_file_metadata(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    metadata = {
        'name': file.name,
        'size': file.size,
        'extension': file.extension,
        'created_at': file.created_at,
        'updated_at': file.updated_at,
    }
    return JsonResponse(metadata)

@login_required
def list_files(request, parent_id=None):
    """
    List files and subfolders within a given parent folder. 
    If no parent_id is provided, show root files and folders.
    """
    parent_folder = None
    if parent_id:
        parent_folder = get_object_or_404(Folder, id=parent_id, owner=request.user)

    # Retrieve folders and files in the current folder
    folders = Folder.objects.filter(owner=request.user, parent=parent_folder)
    files = File.objects.filter(owner=request.user, parent_folder=parent_folder)

    # Collect breadcrumbs for navigation
    breadcrumbs = parent_folder.get_ancestors() if parent_folder else []

    context = {
        'folders': folders,
        'files': files,
        'parent_folder': parent_folder,
        'breadcrumbs': breadcrumbs,
    }
    return render(request, 'folder_management/list_folders.html', context)