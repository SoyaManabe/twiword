from django.contrib import admin

from .models import Words
from .models import Users

admin.site.register(Words)
admin.site.register(Users)