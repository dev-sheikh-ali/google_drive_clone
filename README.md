# Google Drive Clone

### Google drive application clone made with Django

### DEMO: [Google Drive Clone]()

<table width="100%"> 
<tr>
<td width="50%">      
&nbsp; 
<br>
<p align="center">
  ADMIN
</p>
<kbd><img src="./images/admin.png" /></kbd>
</td> 
<td width="50%">
<br>
<p align="center">
  CLIENT
</p>
<img src="./images/drive.png">  
</td>
</table>

## Tech Stack
- **Backend:** Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default)
- **Authentication:** Custom User Model
- **Libraries:** Font Awesome for icons, jQuery for interactivity
- **Django-Jazzmin:** template for django admin `https://django-jazzmin.readthedocs.io/`

## Project Structure

```
user@user:~/Documents/JUNIA 2024/python course/Django_Projects/google_drive_clone$ tree -I "env|venv|server|__pycache__|migrations|images"
.
├── db.sqlite3
├── file_management
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── file_management
│   │       ├── delete_file_modal.html
│   │       ├── list_files.html
│   │       └── upload_file_modal.html
│   ├── templatetags
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── folder_management
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── templates
│   │   └── folder_management
│   │       ├── copy_folder_modal.html
│   │       ├── create_folder_modal.html
│   │       ├── create_subfolder_modal.html
│   │       ├── delete_folder_modal.html
│   │       ├── edit_folder_modal.html
│   │       ├── list_folders.html
│   │       └── move_folder_modal.html
│   ├── templatetags
│   │   ├── folder_tags.py
│   │   └── __init__.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── google_drive_clone
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── README.md
├── requirements.txt
└── user_management
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── __init__.py
    ├── models.py
    ├── templates
    │   ├── home.css
    │   ├── home.html
    │   └── user_management
    │       ├── login.html
    │       ├── password_reset_complete.html
    │       ├── password_reset_confirm.html
    │       ├── password_reset_done.html
    │       ├── password_reset_form.html
    │       ├── profile.html
    │       └── signup.html
    ├── tests.py
    ├── urls.py
    └── views.py

12 directories, 53 files
user@user:~/Documents/JUNIA 2024/python course/Django_Projects/google_drive_clone$ 
    
```

## Run these Commands

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Step 1: Clone the repository
```bash
git clone https://github.com/dev-sheikh-ali/google_drive_clone.git
```

### Step 2: Navigate to the cloned directory
```bash
cd google_drive_clone
```

### Step 3: Create a virtual environment
```bash
python3 -m venv env
```

### Step 4: Activate the virtual environment
- On macOS/Linux:
```bash
source env/bin/activate
```
- On Windows:
```bash
env\Scripts\activate
```

### Step 5: Install Python dependencies
```bash
pip install -r requirements.txt
```

### Step 6: Run database migrations
```bash
python manage.py migrate
```

### Step 7: Create a superuser (optional)
```bash
python manage.py createsuperuser
```

### Step 8: Run the server
```bash
python manage.py runserver
```

### Step 9: Access the application
Open your browser and go to `http://127.0.0.1:8000/signup` to create a new account or `http://127.0.0.1:8000/login` to log in.



### Features 

The web application will provide the maximum of the following features:

1. **Authentication and Account Management**
   - [ ] Account creation with login and password
   - [ ] User authentication for login/logout

2. **File and Folder Management**
   - [ ] Browse files and folders on a web UI
   - [ ] Display file properties and metadata
   - [ ] Upload files (max upload size: 40 MB)
   - [ ] Create folders
   - [ ] Move files and folders
   - [ ] Copy files and folders

3. **Account Storage Limitations**
   - [ ] Drive limit of 100 MB per account
   - [ ] Enforce maximum storage limit (no folder exceeding 100 MB)

4. **Account Information and Statistics**
   - [ ] Account info screen displaying statistics
   - [ ] Space distribution per file format (images, documents, videos, etc.) using graphics

5. **File Preview**
   - [ ] Preview known formats (images, videos, PDFs, source code, documents, etc.)
   - [ ] Open text, view images, play videos

6. **Setup and Installation**
   - [ ] Setup script to install requirements
   - [ ] Demo data setup in SQLite

7. **User Experience (UX)**
   - [ ] Nice, beautiful, responsive UX
   - [ ] Demo compatibility on laptop and smartphone




## Features To Implement later
- search feature
- Trash functionality   *
- favourites / starred files
- file sharinng         *

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
