# Google Drive Clone

#### Use `/login` to access the application and manage your files. Use `python manage.py createsuperuser` to create admin login details for managing users.

## DEMO: [Google Drive Clone]()

<kbd><img src="image" /></kbd>

## Tech Stack
- **Backend:** Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default), can be configured to use PostgreSQL or MySQL
- **Authentication:** Custom User Model
- **Libraries:** Font Awesome for icons, jQuery for interactivity
- **Django-Jazzmin:** template for django admin `https://django-jazzmin.readthedocs.io/`

## Project Structure
```
sheikh@sheikh:~/Documents/JUNIA 2024/python course/Django_Projects/google_drive_clone$ ls
db.sqlite3  file_management    google_drive_clone  README.md
env         folder_management  manage.py           user_management
sheikh@sheikh:~/Documents/JUNIA 2024/python course/Django_Projects/google_drive_clone$ for dir in ./user_management ./file_management ./folder_management; do   tree "$dir"; done
./user_management
├── admin.py
├── apps.py
├── forms.py
├── __init__.py
├── migrations
│   ├── 0001_initial.py
│   ├── __init__.py
│   └── __pycache__
│       ├── 0001_initial.cpython-310.pyc
│       └── __init__.cpython-310.pyc
├── models.py
├── __pycache__
│   ├── admin.cpython-310.pyc
│   ├── apps.cpython-310.pyc
│   ├── forms.cpython-310.pyc
│   ├── __init__.cpython-310.pyc
│   ├── models.cpython-310.pyc
│   ├── urls.cpython-310.pyc
│   └── views.cpython-310.pyc
├── templates
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

5 directories, 27 files
./file_management
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   ├── __init__.py
│   └── __pycache__
│       └── __init__.cpython-310.pyc
├── models.py
├── __pycache__
│   ├── admin.cpython-310.pyc
│   ├── apps.cpython-310.pyc
│   ├── __init__.cpython-310.pyc
│   └── models.cpython-310.pyc
├── tests.py
└── views.py

3 directories, 12 files
./folder_management
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   ├── __init__.py
│   └── __pycache__
│       └── __init__.cpython-310.pyc
├── models.py
├── __pycache__
│   ├── admin.cpython-310.pyc
│   ├── apps.cpython-310.pyc
│   ├── __init__.cpython-310.pyc
│   └── models.cpython-310.pyc
├── tests.py
└── views.py

3 directories, 12 files

    
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

## Features
- User registration and authentication
- File and folder management
- Dark and light mode toggle
- Profile management

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
