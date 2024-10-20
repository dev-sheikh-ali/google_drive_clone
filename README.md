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

## Project Structure
```
google_drive_clone/
    ├── drive_clone/
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   ├── wsgi.py
    ├── user_management/
    │   ├── migrations/
    │   ├── templates/
    │   │   └── user_management/
    │   │       ├── signup.html
    │   │       ├── login.html
    │   │       ├── profile.html
    │   ├── static/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── views.py
    │   ├── forms.py
    │   ├── urls.py
    ├── folder_management/
    │   ├── migrations/
    │   ├── templates/
    │   │   └── folder_management/
    │   │       ├── folder_list.html
    │   │       ├── create_folder.html
    │   │       ├── folder_detail.html
    │   ├── static/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    ├── file_management/
    │   ├── migrations/
    │   ├── templates/
    │   │   └── file_management/
    │   │       ├── upload_file.html
    │   │       ├── file_list.html
    │   │       ├── file_detail.html
    │   ├── static/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── views.py
    │   ├── urls.py
    ├── media/  
    ├── uploads/  # Directory for uploaded files
    ├── manage.py
    └── env/  # Virtual environment
    
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
Open your browser and go to `http://127.0.0.1:8000/user/signup` to create a new account or `http://127.0.0.1:8000/user/login` to log in.

## Features
- User registration and authentication
- File and folder management
- Dark and light mode toggle
- Profile management

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
