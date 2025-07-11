# create_superuser.py
import os
import django
from django.contrib.auth import get_user_model

# Replace this with your actual settings module if different
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TEAFARM01BACKEND.settings")
django.setup()

User = get_user_model()

username = "admin"
email = "lonewalker634@gmail.com"
password = "434wxg79"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"✅ Superuser '{username}' created.")
else:
    print(f"ℹ️ Superuser '{username}' already exists.")
