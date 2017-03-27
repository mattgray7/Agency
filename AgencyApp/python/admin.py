from django.contrib import admin

# Register your models here.
from models import User, Posting

admin.site.register(User)
admin.site.register(Posting)