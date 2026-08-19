from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = "Create a default superuser if none exists"

    def handle(self, *args, **kwargs):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "osim")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "osimemmanuel2@gmail.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "kidzoom123")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser {username} created"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser {username} already exists"))
