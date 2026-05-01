import os
from django.conf import settings
from django.http import HttpResponse

def home_view(request):
    """
    Serves the premium landing page from the frontend directory.
    """
    file_path = os.path.join(settings.BASE_DIR, 'frontend', 'index.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content)

def static_view(request):
    """
    Serves the CSS for the landing page.
    """
    file_path = os.path.join(settings.BASE_DIR, 'frontend', 'style.css')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/css')

def portal_view(request):
    """
    Serves the premium student portal page.
    """
    file_path = os.path.join(settings.BASE_DIR, 'frontend', 'portal.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content)

def portal_static_view(request):
    """
    Serves the CSS for the student portal.
    """
    file_path = os.path.join(settings.BASE_DIR, 'frontend', 'portal.css')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/css')
