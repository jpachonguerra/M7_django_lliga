from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from futbol.models import *

admin.site.register(Lliga)

class EquipAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        if request.user.is_superuser:
            return Equip.objects.all()
        user = request.user
        equips = user.equips.all()
        equips_ids = [e.id for e in equips]
        qs = Equip.objects.filter(pk__in=equips_ids)
        return qs

admin.site.register(Equip, EquipAdmin)

class JugadorAdmin(admin.ModelAdmin):
    search_fields = ("nom","equip_nom")

admin.site.register(Jugador, JugadorAdmin)

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

class UsuariAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("lliga", {
            "fields": ["equips", "telefon"]
            }
        ),
    )
    filter_horizontal = UserAdmin.filter_horizontal + ('equips',)

admin.site.register(Usuari, UsuariAdmin)

