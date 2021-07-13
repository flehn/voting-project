from django.contrib import admin
from .models import Profile

# Hier wird das erstelle Profile Model registriert damit man per admin Seite darauf zugreifen kann.
admin.site.register(Profile)
