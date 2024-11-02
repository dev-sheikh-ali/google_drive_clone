from django import template

register = template.Library()

@register.filter
def file_icon(extension):
    """
    Returns the appropriate FontAwesome icon class based on file extension.
    """
    icons = {
        '.png': 'fas fa-file-image',
        '.jpg': 'fas fa-file-image',
        '.jpeg': 'fas fa-file-image',
        '.gif': 'fas fa-file-image',
        '.bmp': 'fas fa-file-image',
        '.svg': 'fas fa-file-image',
        '.mp4': 'fas fa-file-video',
        '.avi': 'fas fa-file-video',
        '.mov': 'fas fa-file-video',
        '.mkv': 'fas fa-file-video',
        '.webm': 'fas fa-file-video',
        '.pdf': 'fas fa-file-pdf',
        '.doc': 'fas fa-file-word',
        '.docx': 'fas fa-file-word',
        '.xls': 'fas fa-file-excel',
        '.xlsx': 'fas fa-file-excel',
        '.ppt': 'fas fa-file-powerpoint',
        '.pptx': 'fas fa-file-powerpoint',
        '.txt': 'fas fa-file-alt',
        '.csv': 'fas fa-file-csv',
        '.zip': 'fas fa-file-archive',
        '.rar': 'fas fa-file-archive',
        '.7z': 'fas fa-file-archive',
        '.tar': 'fas fa-file-archive',
        '.gz': 'fas fa-file-archive',
        '.mp3': 'fas fa-file-audio',
        '.wav': 'fas fa-file-audio',
        '.ogg': 'fas fa-file-audio',
        '.flac': 'fas fa-file-audio',
        '.py': 'fas fa-file-code',
        '.js': 'fas fa-file-code',
        '.html': 'fas fa-file-code',
        '.css': 'fas fa-file-code',
        '.json': 'fas fa-file-code',
        '.xml': 'fas fa-file-code',
    }
    return icons.get(extension.lower(), 'fas fa-file')
