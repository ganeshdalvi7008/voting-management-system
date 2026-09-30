# Voting Management System - Django

Converted from the supplied PHP + MySQL voting system to Python/Django.

## Features
- Voter registration, login, logout and profile
- Admin/staff dashboard
- Election create/edit/start/stop/delete
- Candidate create/edit/delete/status toggle and photo upload
- Voter registry/search/status toggle
- One vote per voter per election
- Results for completed elections with vote share and tie handling
- Django password hashing
- Django ORM + SQLite by default
- Django admin panel

## Run
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

To use MySQL, install `mysqlclient` or `PyMySQL` and change DATABASES in `voting_project/settings.py`.
