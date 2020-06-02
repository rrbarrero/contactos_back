from django.contrib import admin
from .models import *

class TratamientoAdmin(admin.ModelAdmin):
    pass

class ProvinciaAdmin(admin.ModelAdmin):
    pass

class PaisAdmin(admin.ModelAdmin):
    pass

class ColectivoAdmin(admin.ModelAdmin):
    pass

class SubColectivoAdmin(admin.ModelAdmin):
    pass

class PersonaAdmin(admin.ModelAdmin):

    search_fields = ['nombre', 'apellidos']


class CargoAdmin(admin.ModelAdmin):

    list_display = ('persona', 'cargo', 'empresa')
    search_fields = ['cargo', 'empresa', 'persona__nombre', 'persona__apellidos']


class TelefonoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tratamiento, TratamientoAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Colectivo, ColectivoAdmin)
admin.site.register(SubColectivo, SubColectivoAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Telefono, TelefonoAdmin)
