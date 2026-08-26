# BM-EVENTS2

Scaffolded Django project for BM Events platform.

Quick start (Windows):

1. Create a virtualenv and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run migrations and start server:

```powershell
python manage.py migrate
python manage.py runserver
```

This initial scaffold includes a custom `User` model in the `accounts` app and basic templates/static wiring. Next steps: implement `vendors`, `bookings`, `reviews` apps and wire the full frontend design from `index.html`.
