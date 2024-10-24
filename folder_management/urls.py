
from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_folders, name='list_folders'),
    path('<int:parent_id>/', views.list_folders, name='list_folders_nested'),
    path('create/', views.create_folder, name='create_folder'),
    path('<int:parent_id>/create/', views.create_folder, name='create_folder_nested'),
    path('<int:folder_id>/update/', views.update_folder, name='update_folder'),
    path('<int:folder_id>/delete/', views.delete_folder, name='delete_folder'),
    path('<int:folder_id>/move/', views.move_folder, name='move_folder'),
    path('<int:folder_id>/copy/', views.copy_folder, name='copy_folder'),
]
