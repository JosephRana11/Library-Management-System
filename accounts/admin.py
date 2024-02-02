from django.contrib import admin
from .models import User

#registering User model to Admin Panel
admin.site.register(User)