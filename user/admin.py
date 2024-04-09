from django.contrib.auth.models import Group
from django.contrib import admin
from .models import User, Province


admin.site.register(User)
admin.site.register(Province)
