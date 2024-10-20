from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.http import JsonResponse
import re

@login_required
def home(request):
    # Dummy data for files and folders
    files = [
        {'name': 'Document1.pdf', 'type': 'pdf', 'size': '1.2MB'},
        {'name': 'Image1.jpg', 'type': 'image', 'size': '500KB'},
        {'name': 'Presentation.pptx', 'type': 'ppt', 'size': '2.4MB'},
        {'name': 'Spreadsheet.xlsx', 'type': 'excel', 'size': '800KB'},
    ]
    
    folders = [
        {'name': 'Projects', 'icon': 'folder'},
        {'name': 'Photos', 'icon': 'folder'},
        {'name': 'Music', 'icon': 'folder'},
        {'name': 'Documents', 'icon': 'folder'},
    ]

    return render(request, 'home.html', {'files': files, 'folders': folders})

def signup(request):
    if request.method == 'POST':
        print("Processing signup...")
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate form data
        errors = []
        if CustomUser.objects.filter(username=username).exists():
            errors.append("This username is already taken.")
        if CustomUser.objects.filter(email=email).exists():
            errors.append("A user with this email already exists.")
        if password1 != password2:
            errors.append("Passwords do not match.")
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password1):
            errors.append("Password must be at least 8 characters long and contain both letters and numbers.")

        # If there are errors, show them to the user
        if errors:
            for error in errors:
                messages.error(request, error)
            print(f"Errors encountered: {errors}")  # Debugging output
            return render(request, 'user_management/signup.html', {'form': CustomUserCreationForm()})

        # Create user instance
        user = CustomUser(username=username, email=email, password=make_password(password1))
        user.save()  # Save user
        print("User created successfully.")  # Debugging output
        login(request, user)  # Log the user in
        messages.success(request, "Account created successfully!")
        return redirect('home')
    
    form = CustomUserCreationForm()
    return render(request, 'user_management/signup.html', {'form': form})

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'available': CustomUser.objects.filter(username=username).count() == 0,
        'message': 'Username is available!' if username and CustomUser.objects.filter(username=username).count() == 0 else 'Username is taken.'
    }
    return JsonResponse(data)

def login_view(request):
    if request.method == 'POST':
        identifier = request.POST.get('username_or_email')
        password = request.POST.get('password')

        # Check if identifier or password is None
        if not identifier or not password:
            messages.error(request, "Please enter your username or email and password.")
            return render(request, 'user_management/login.html')

        user = None
        if '@' in identifier:
            try:
                user = CustomUser.objects.get(email=identifier)
                user = authenticate(request, username=user.username, password=password)
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid email or password.")
        else:
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'user_management/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'user_management/profile.html', {'form': form})
