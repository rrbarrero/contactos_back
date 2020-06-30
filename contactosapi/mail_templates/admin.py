from django.contrib import admin
from .models import *

class PlantillaAdmin(admin.ModelAdmin):
    pass

admin.site.register(Plantilla, PlantillaAdmin)
