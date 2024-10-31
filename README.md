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
- Authentication and account creation with login and password
- Browse folders on a web UI
- Create , edit , delete , copy and move folders
- Dark and light mode toggle
- Profile management

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
