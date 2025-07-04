import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shoppit.settings")
django.setup()

User = get_user_model()

username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "johnson")
email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "ibitoyejohnson234@gmail.com")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "jay321125")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created.")
else:
    print("Superuser already exists.")
