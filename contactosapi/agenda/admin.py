from django.contrib import admin
from .models import *


class ColectivoAdmin(admin.ModelAdmin):
    pass

class SubColectivoAdmin(admin.ModelAdmin):
    pass

class PersonaAdmin(admin.ModelAdmin):
    pass

class CargoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Colectivo, ColectivoAdmin)
admin.site.register(SubColectivo, SubColectivoAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Cargo, CargoAdmin)