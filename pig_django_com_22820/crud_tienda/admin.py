from django.contrib import admin
from .models import Vestimenta, Calzado, Suplemento, Accesorio, Opciones_vestimenta, Opciones_calzado

# Register your models here.

class Opciones_vestimentaInline(admin.TabularInline):
    model = Opciones_vestimenta

class VestimentaAdmin(admin.ModelAdmin):
    list_display = ("nombre","precio","foto","info","sexo") # campos q aparecen
    fields = ['nombre','foto','precio',('sexo', 'subcategoria'),'info'] # orden (si los meto en una tupla (a,b,c) los muestra en horizontal)
    search_fields = ('nombre',)
    list_filter = ("precio","sexo")
    inlines = [
        Opciones_vestimentaInline,
    ]

class Opciones_calzadoInline(admin.TabularInline):
    model = Opciones_calzado

class CalzadoAdmin(admin.ModelAdmin):
    list_display = ("nombre","precio","foto","info","sexo") # campos q aparecen
    fields = ['nombre','foto','precio',('sexo'),'info'] # orden (si los meto en una tupla (a,b,c) los muestra en horizontal)
    search_fields = ('nombre',)
    list_filter = ("precio","sexo")
    inlines = [
        Opciones_calzadoInline,
    ]

#class SuplementoAdmin(admin.ModelAdmin)

admin.site.register(Vestimenta, VestimentaAdmin)
admin.site.register(Calzado, CalzadoAdmin)
admin.site.register(Suplemento)#, SuplementoAdmin)
admin.site.register(Accesorio)