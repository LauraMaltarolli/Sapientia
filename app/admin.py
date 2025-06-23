# app/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Usuario, Dilema, SessaoReflexao, Mensagem, TesteFilosofico,
    ResultadoTeste, TeoriaFilosofica, DilemaCriado, Filosofo, AcaoAnalisada
)

class MensagemInline(admin.TabularInline):
    model = Mensagem
    extra = 1
    readonly_fields = ('remetente', 'conteudo', 'timestamp')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Personalizados', {'fields': ('data_nascimento',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos Personalizados', {'fields': ('data_nascimento',)}),
    )

@admin.register(SessaoReflexao)
class SessaoReflexaoAdmin(admin.ModelAdmin):
    list_display = ('dilema', 'usuario', 'data_inicio')
    search_fields = ('dilema__titulo', 'usuario__username')
    inlines = [MensagemInline]

@admin.register(Dilema)
class DilemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_criacao')
    search_fields = ('titulo',)

# Registro dos outros modelos
admin.site.register(Mensagem)
admin.site.register(TesteFilosofico)
admin.site.register(ResultadoTeste)
admin.site.register(TeoriaFilosofica)
admin.site.register(DilemaCriado)
admin.site.register(Filosofo)
admin.site.register(AcaoAnalisada)