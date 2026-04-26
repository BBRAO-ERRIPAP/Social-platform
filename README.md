# SocialHub — Django Social Media Platform

A full-featured social media platform built with Django, Django REST Framework, and Bootstrap 5.

## Features

- User registration, login, and profile editing
- Create, like, and comment on posts with image uploads
- Follow/unfollow users and send friend requests
- Real-time-style notifications (likes, comments, follows, friend requests)
- REST API for all core features
- Responsive UI with Bootstrap 5
- Django admin interface
- Search for users

## Tech Stack

- Python 3.10+
- Django 4.2
- Django REST Framework
- SQLite (dev) / PostgreSQL (prod)
- Bootstrap 5 + Bootstrap Icons
- WhiteNoise for static files
- Gunicorn for production

## Setup

```bash
git clone https://github.com/yourname/social-platform.git
cd social_platform

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# Edit .env with your values

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000

## Project Structure
social_platform/
├── users/          # Auth, profiles, search
├── posts/          # Posts, comments, likes
├── friends/        # Follow, friend requests
├── notifications/  # Notification system
├── api/            # REST API (DRF)
├── templates/      # HTML templates
├── static/         # CSS, JS
└── tests/          # Test suite
## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | /api/posts/ | List or create posts |
| GET/DELETE | /api/posts/<id>/ | Post detail |
| POST | /api/posts/<id>/like/ | Toggle like |
| GET/POST | /api/posts/<id>/comments/ | Comments |
| GET | /api/users/ | List/search users |
| GET | /api/users/<username>/ | User detail |
| POST | /api/users/<username>/follow/ | Toggle follow |

## Running Tests

```bash
python manage.py test tests/
```