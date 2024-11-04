# file_management/context_processors.py
from django.db import models  # Add this import
from .models import File
from django.conf import settings

def storage_stats(request):
    if request.user.is_authenticated:
        # Calculate used storage and max storage
        used_storage = File.objects.filter(owner=request.user).aggregate(total_size=models.Sum('size'))['total_size'] or 0
        max_storage = settings.USER_MAX_STORAGE
        used_percentage = (used_storage / max_storage) * 100 if max_storage > 0 else 0

        return {
            'used_storage': used_storage,
            'max_storage': max_storage,
            'used_percentage': used_percentage
        }
    return {}
