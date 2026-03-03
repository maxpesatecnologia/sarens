from django.contrib import admin
from django.utils.html import format_html
from .models import PerfilAnalista, Equipamento, Lead, Operacao, Financeiro


# ================================================================
#  EQUIPAMENTO
# ================================================================
@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display  = ['nome', 'categoria_badge', 'capacidade', 'ativo_badge']
    list_filter   = ['categoria', 'ativo']
    search_fields = ['nome']

    @admin.display(description='Categoria')
    def categoria_badge(self, obj):
        cores = {
            'guindastes':    'bg-blue-100 text-blue-800',
            'munck':         'bg-purple-100 text-purple-800',
            'empilhadeira':  'bg-orange-100 text-orange-800',
            'linha-amarela': 'bg-yellow-100 text-yellow-800',
        }
        classe = cores.get(obj.categoria, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 rounded-full text-xs font-semibold {}">{}</span>',
            classe, obj.get_categoria_display()
        )

    @admin.display(description='Ativo')
    def ativo_badge(self, obj):
        if obj.ativo:
            return format_html('<span class="px-2 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800">✓ Ativo</span>')
        return format_html('<span class="px-2 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800">✗ Inativo</span>')


# ================================================================
#  LEAD
# ================================================================
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display  = ['nome', 'email', 'telefone', 'categoria_badge', 'subcategoria', 'status_badge', 'analista_responsavel', 'criado_em']
    list_filter   = ['status', 'categoria', 'analista_responsavel']
    search_fields = ['nome', 'email']

    @admin.display(description='Status')
    def status_badge(self, obj):
        cores = {
            'novo':           '#0c0a09',
            'em_atendimento': '#eab308',
            'fechado':        '#16a34a',
            'perdido':        '#dc2626',
        }
        classe = cores.get(obj.status, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 rounded-full text-xs font-semibold {}">{}</span>',
            classe, obj.get_status_display()
        )

    @admin.display(description='Categoria')
    def categoria_badge(self, obj):
        cores = {
            'guindastes':    'bg-blue-100 text-blue-800',
            'munck':         'bg-purple-100 text-purple-800',
            'empilhadeira':  'bg-orange-100 text-orange-800',
            'linha-amarela': 'bg-yellow-100 text-yellow-800',
            'outro':         'bg-gray-100 text-gray-800',
        }
        classe = cores.get(obj.categoria, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 rounded-full text-xs font-semibold {}">{}</span>',
            classe, obj.get_categoria_display()
        )


# ================================================================
#  OPERAÇÃO
# ================================================================
@admin.register(Operacao)
class OperacaoAdmin(admin.ModelAdmin):
    list_display  = ['lead', 'equipamento', 'data_inicio', 'data_fim', 'turno_badge', 'duracao']
    list_filter   = ['turno', 'equipamento']

    @admin.display(description='Turno')
    def turno_badge(self, obj):
        cores = {
            'diurno':  'bg-yellow-100 text-yellow-800',
            'noturno': 'bg-indigo-100 text-indigo-800',
            '24h':     'bg-green-100 text-green-800',
        }
        classe = cores.get(obj.turno, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 rounded-full text-xs font-semibold {}">{}</span>',
            classe, obj.get_turno_display()
        )

    @admin.display(description='Duração')
    def duracao(self, obj):
        return format_html(
            '<span class="text-xs text-gray-500">{} dias</span>',
            obj.duracao_dias
        )


# ================================================================
#  FINANCEIRO
# ================================================================
@admin.register(Financeiro)
class FinanceiroAdmin(admin.ModelAdmin):
    list_display  = ['operacao', 'receita_fmt', 'despesa_fmt', 'margem_fmt', 'status_pgto_badge']
    list_filter   = ['status_pgto']

    @admin.display(description='Receita')
    def receita_fmt(self, obj):
        return format_html(
            '<span class="font-semibold text-green-700">R$ {}</span>',
            f'{obj.receita:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )

    @admin.display(description='Despesa')
    def despesa_fmt(self, obj):
        return format_html(
            '<span class="text-red-600">R$ {}</span>',
            f'{obj.despesa:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        )

    @admin.display(description='Margem')
    def margem_fmt(self, obj):
        cor = 'text-green-700' if obj.margem >= 0 else 'text-red-600'
        return format_html(
            '<span class="font-bold {}">R$ {} ({}%)</span>',
            cor,
            f'{obj.margem:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
            obj.margem_percentual
        )

    @admin.display(description='Pagamento')
    def status_pgto_badge(self, obj):
        cores = {
            'pendente': 'bg-red-100 text-red-800',
            'parcial':  'bg-yellow-100 text-yellow-800',
            'pago':     'bg-green-100 text-green-800',
        }
        classe = cores.get(obj.status_pgto, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 rounded-full text-xs font-semibold {}">{}</span>',
            classe, obj.get_status_pgto_display()
        )


# ================================================================
#  PERFIL ANALISTA
# ================================================================
@admin.register(PerfilAnalista)
class PerfilAnalistaAdmin(admin.ModelAdmin):
    list_display  = ['user', 'cargo_badge', 'telefone', 'metricas', 'ativo_badge']
    list_filter   = ['cargo', 'ativo']

    @admin.display(description='Cargo')
    def cargo_badge(self, obj):
        cores = {
            'gerente':     'bg-yellow-100 text-yellow-800',
            'coordenador': 'bg-blue-100 text-blue-800',
            'analista_sr': 'bg-green-100 text-green-800',
            'analista_pl': 'bg-indigo-100 text-indigo-800',
            'analista_jr': 'bg-gray-100 text-gray-800',
        }
        classe = cores.get(obj.cargo, 'bg-gray-100 text-gray-800')
        return format_html(
            '<span class="px-2 py-1 rounded-full text-xs font-semibold {}">{}</span>',
            classe, obj.get_cargo_display()
        )

    @admin.display(description='Performance')
    def metricas(self, obj):
        return format_html(
            '<span class="text-xs">{} leads · {} fechados · <strong>{}%</strong> conv.</span>',
            obj.total_leads, obj.leads_fechados, obj.taxa_conversao
        )

    @admin.display(description='Ativo')
    def ativo_badge(self, obj):
        if obj.ativo:
            return format_html('<span class="px-2 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-800">✓ Ativo</span>')
        return format_html('<span class="px-2 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800">✗ Inativo</span>')