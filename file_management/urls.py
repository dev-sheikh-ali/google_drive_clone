# file_management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/<int:parent_id>/', views.upload_file, name='upload_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('list/<int:parent_id>/', views.list_files, name='list_files'),  # Ensure list_files is defined here
    path('<int:file_id>/metadata/', views.view_file_metadata, name='view_file_metadata'),
]
