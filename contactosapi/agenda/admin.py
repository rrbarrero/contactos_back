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

    list_display = ('persona', 'cargo', 'empresa', 'finalizado')
    search_fields = ['cargo', 'empresa', 'persona__nombre', 'persona__apellidos']


class TelefonoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'numero')
    search_fields = ['nombre', 'cargo__empresa', 'cargo__persona__nombre', 'cargo__persona__apellidos', 'cargo__cargo']

class CorreoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tratamiento, TratamientoAdmin)
admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Pais, PaisAdmin)
admin.site.register(Colectivo, ColectivoAdmin)
admin.site.register(SubColectivo, SubColectivoAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Telefono, TelefonoAdmin)
admin.site.register(Correo, CorreoAdmin)
