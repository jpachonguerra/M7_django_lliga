from django.contrib import admin

# Register your models here.
from futbol.models import *

admin.site.register(Lliga)
admin.site.register(Equip)
admin.site.register(Jugador)

class EventInline(admin.TabularInline):
    model = Event
    extra = 2

class PartitAdmin(admin.ModelAdmin):
    list_display = ("equip_local","equip_visitant","data","gols_local","gols_visitant")
    fields = ("lliga","equip_local","equip_visitant","data","gols_local","gols_visitant")
    readonly_fields = ("gols_local","gols_visitant")
    search_fields = ("equip_local__nom","equip_visitant__nom")
    inlines = [EventInline,]

admin.site.register(Partit, PartitAdmin)
