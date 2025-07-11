# create_superuser.py
import os
import django
from django.contrib.auth import get_user_model

# Replace this with your actual settings module if different
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TEAFARM01BACKEND.settings")
django.setup()

User = get_user_model()

email = "lonewalker634@gmail.com"
password = "434wxg79"
phone_number = "0770635336"  # <-- REQUIRED, must be unique
name = "admin"  # optional

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        email=email,
        password=password,
        phone_number=phone_number,
        name=name,
        is_staff=True,
        is_superuser=True
    )
    print(f"✅ Superuser '{email}' created.")
else:
    print(f"ℹ️ Superuser '{email}' already exists.")
