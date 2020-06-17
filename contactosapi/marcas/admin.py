from django.contrib import admin
from .models import Marca

class MarcaAdmin(admin.ModelAdmin):

    raw_id_fields = ("contactos",)
    list_display = ('nombre',)
    search_fields = ['contactos__persona__nombre']


admin.site.register(Marca, MarcaAdmin)