from django.shortcuts import render
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Sum, F, Count
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Lead, Operacao, Financeiro, PerfilAnalista

@staff_member_required
def dashboard(request):
    hoje = timezone.localdate()
    mes  = hoje.month
    ano  = hoje.year

    # ── KPIs ──────────────────────────────────────────────
    leads_mes          = Lead.objects.filter(criado_em__month=mes, criado_em__year=ano).count()
    leads_total        = Lead.objects.count()
    leads_fechados     = Lead.objects.filter(status='fechado').count()
    leads_sem_analista = Lead.objects.filter(analista_responsavel__isnull=True, status='novo').count()
    taxa_conversao     = round((leads_fechados / leads_total * 100), 1) if leads_total > 0 else 0

    operacoes_ativas   = Operacao.objects.filter(data_inicio__lte=hoje, data_fim__gte=hoje).count()

    fin_mes = Financeiro.objects.filter(
        operacao__data_inicio__month=mes,
        operacao__data_inicio__year=ano
    ).aggregate(
        total_receita=Sum('receita'),
        total_despesa=Sum('despesa'),
    )

    def fmt(val):
        if val is None:
            return '0,00'
        return f'{val:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')

    r = fin_mes['total_receita'] or 0
    d = fin_mes['total_despesa'] or 0
    receita_mes = fmt(r)
    margem_mes  = fmt(r - d)

    # ── Leads por categoria ───────────────────────────────
    CORES = {
        'guindastes':    '#3b82f6',
        'munck':         '#a855f7',
        'empilhadeira':  '#f97316',
        'linha-amarela': '#eab308',
        'outro':         '#6b7280',
    }

    leads_por_categoria = []
    for cat in Lead.objects.values('categoria').annotate(total=Count('id')).order_by('-total'):
        leads_por_categoria.append({
            'nome':  dict(Lead.Categoria.choices).get(cat['categoria'], cat['categoria']),
            'total': cat['total'],
            'cor':   CORES.get(cat['categoria'], '#6b7280'),
        })

    # ── Leads sem analista ────────────────────────────────
    leads_novos = Lead.objects.filter(
        analista_responsavel__isnull=True,
        status='novo'
    ).order_by('-criado_em')[:8]

    # ── Operações em andamento ────────────────────────────
    operacoes_andamento = Operacao.objects.filter(
        data_inicio__lte=hoje,
        data_fim__gte=hoje
    ).select_related('lead', 'equipamento').order_by('data_fim')[:8]

    # ── Ranking de analistas ──────────────────────────────
    ranking_analistas = []
    for perfil in PerfilAnalista.objects.filter(ativo=True).select_related('user'):
        if perfil.total_leads > 0:
            ranking_analistas.append({
                'nome':      perfil.user.get_full_name() or perfil.user.username,
                'leads':     perfil.total_leads,
                'fechados':  perfil.leads_fechados,
                'conversao': perfil.taxa_conversao,
            })
    ranking_analistas.sort(key=lambda x: x['conversao'], reverse=True)

    # ── Contexto de Renderização ──────────────────────────
    context = {
        'leads_mes':            leads_mes,
        'leads_total':          leads_total,
        'leads_fechados':       leads_fechados,
        'leads_sem_analista':   leads_sem_analista,
        'taxa_conversao':       taxa_conversao,
        'operacoes_ativas':     operacoes_ativas,
        'receita_mes':          receita_mes,
        'margem_mes':           margem_mes,
        'leads_por_categoria':  leads_por_categoria,
        'leads_novos':          leads_novos,
        'operacoes_andamento':  operacoes_andamento,
        'ranking_analistas':    ranking_analistas,
        'title':                'Dashboard', # Define o título no cabeçalho do sistema
        'receita_grafico':      float(r),
        'despesa_grafico':      float(d),
    }
    context.update(admin.site.each_context(request))
    return render(request, 'admin/dashboard.html', context)

    # Esta linha injeta o menu lateral e as permissões do sistema Admin
    context.update(admin.site.each_context(request))

    return render(request, 'admin/dashboard.html', context)


# ── API de contatos ──────────────────────────────────────────
@csrf_exempt
def receber_contato(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Lead.objects.create(
                nome=data.get('nome', ''),
                email=data.get('email', ''),
                telefone=data.get('telefone', ''),
                categoria=data.get('categoria', 'outro'),
                subcategoria=data.get('subcategoria', 'outro'),
                mensagem=data.get('mensagem', ''),
            )
            return JsonResponse({'status': 'sucesso', 'mensagem': 'Lead salvo com sucesso!'}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'erro', 'mensagem': str(e)}, status=400)
    return JsonResponse({'status': 'erro', 'mensagem': 'Método não permitido'}, status=405)