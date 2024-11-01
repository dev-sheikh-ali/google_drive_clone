from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_folders, name='home'),  
    path('upload/<int:parent_id>/', views.upload_file, name='upload_file'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('list/<int:parent_id>/', views.list_folders, name='list_folders'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),  # Make sure this is present
]