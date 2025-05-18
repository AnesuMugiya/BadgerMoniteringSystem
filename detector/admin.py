from django.contrib import admin
from .models import ImageFile, Detection

admin.site.register(ImageFile)
admin.site.register(Detection)