from django.contrib import admin
from .models import Lista

class ListaAdmin(admin.ModelAdmin):

    raw_id_fields = ("contactos",)
    list_display = ('nombre', 'contacts_len', 'descripcion')
    search_fields = ['contactos__persona__nombre', 'descripcion']

    def contacts_len(self, obj):
        return "{}".format(len(obj.contactos.all()))
    contacts_len.short_description = 'Contactos incluídos'


admin.site.register(Lista, ListaAdmin)