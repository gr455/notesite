from django.contrib import admin
from .models import *
from django.db import models

# Register your models here.


admin.site.register(Tutorial)
admin.site.register(Note)
admin.site.register(Chapter)
admin.site.register(Course)
admin.site.register(Favourite)