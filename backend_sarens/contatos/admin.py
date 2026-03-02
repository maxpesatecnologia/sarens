from django.contrib import admin
from .models import Solicitacao

@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'assunto', 'data_recebimento') 
    search_fields = ('nome', 'email') 