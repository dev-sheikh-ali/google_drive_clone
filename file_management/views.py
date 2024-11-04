# file_management/views.py
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import File
from folder_management.models import Folder
from .forms import FileUploadForm
from django.db import models
import os
from django.db.models import Sum
from django.conf import settings

MAX_FILE_SIZE = 40 * 1024 * 1024  # 40 MB
USER_MAX_STORAGE = 100 * 1024 * 1024  # 100 MB


@login_required
def dashboard(request):
    # Get all files and folders for the user
    total_files = File.objects.filter(owner=request.user).count()
    total_folders = Folder.objects.filter(owner=request.user).count()

    # Calculate used storage
    used_storage = File.objects.filter(owner=request.user).aggregate(total_size=Sum('size'))['total_size'] or 0
    max_storage = settings.USER_MAX_STORAGE
    used_percentage = (used_storage / max_storage) * 100 if max_storage > 0 else 0

    # Folder storage usage (considering only root folders)
    folders = Folder.objects.filter(owner=request.user, parent=None)  # Get only root folders
    folder_names = []
    folder_sizes = []

    for folder in folders:
        folder_size = File.objects.filter(owner=request.user, parent_folder=folder).aggregate(total_size=Sum('size'))['total_size'] or 0
        folder_names.append(folder.name)
        folder_sizes.append(folder_size / (1024 * 1024))  # Convert to MB

    context = {
        'total_files': total_files,
        'total_folders': total_folders,
        'used_storage': used_storage,
        'max_storage': max_storage,
        'used_percentage': used_percentage,
        'folder_names': folder_names,
        'folder_sizes': folder_sizes,
    }
    return render(request, 'file_management/dashboard.html', context)

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
            file.name = file.file.name  # Set the file name here
            file.save()
            return JsonResponse({"message": "File uploaded successfully!", "file_name": file.name}, status=200)
        else:
            return JsonResponse({"error": "Invalid form submission"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=400)

@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    parent_id = file.parent_folder.id if file.parent_folder else None  # Get parent folder ID

    file_path = file.file.path
    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the file from the server directory

    file.delete()
    messages.success(request, "File deleted successfully!")

    # Redirect based on the presence of a parent folder
    if parent_id:
        return redirect('list_folders_nested', parent_id=parent_id)
    return redirect('list_folders')

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


@login_required
def list_recent_files(request):
    # Fetch the 10 most recent files for the authenticated user
    recent_files = File.objects.filter(owner=request.user).order_by('-created_at')[:10]

    context = {
        'files': recent_files,
        'parent_folder': None,  # No parent folder needed for recent files
        'breadcrumbs': [],  # No breadcrumbs for this section
    }
    return render(request, 'file_management/list_recent_files.html', context)
@login_required
def download_file(request, file_id):
    try:
        # Retrieve the file object that belongs to the requesting user
        file = get_object_or_404(File, id=file_id, owner=request.user)

        # Construct the path to the file
        file_path = file.file.path

        # Ensure the file exists on the server
        if not os.path.exists(file_path):
            raise FileNotFoundError

        # Prepare and return the response to serve the file
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{file.name}"'
        return response

    except File.DoesNotExist:
        return JsonResponse({"error": "File does not exist"}, status=404)
    except FileNotFoundError:
        return JsonResponse({"error": "The file was not found on the server"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)