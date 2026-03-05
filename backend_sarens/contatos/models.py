from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


# ================================================================
#  PERFIL DO ANALISTA — Extensão do User nativo do Django
# ================================================================

class PerfilAnalista(models.Model):

    class Cargo(models.TextChoices):
        ANALISTA_JR = 'analista_jr', 'Analista Comercial Jr.'
        ANALISTA_PL = 'analista_pl', 'Analista Comercial Pl.'
        ANALISTA_SR = 'analista_sr', 'Analista Comercial Sr.'
        COORDENADOR = 'coordenador', 'Coordenador Comercial'
        GERENTE     = 'gerente',     'Gerente Comercial'

    # Vínculo com o User do Django (login, senha, permissões)
    user     = models.OneToOneField(
                 User,
                 on_delete=models.CASCADE,
                 related_name='perfil',
                 verbose_name='Usuário'
               )

    # Dados profissionais
    cargo    = models.CharField(
                 max_length=20,
                 choices=Cargo.choices,
                 default=Cargo.ANALISTA_PL,
                 verbose_name='Cargo'
               )
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone / WhatsApp')
    linkedin = models.URLField(blank=True, verbose_name='LinkedIn (URL)')
    foto     = models.ImageField(
                 upload_to='analistas/',
                 blank=True,
                 null=True,
                 verbose_name='Foto de perfil'
               )
    bio      = models.TextField(
                 blank=True,
                 verbose_name='Bio / Especialidade',
                 help_text='Breve descrição da especialidade do analista'
               )
    ativo    = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Cadastrado em')

    class Meta:
        verbose_name        = 'Perfil do Analista'
        verbose_name_plural = 'Perfis dos Analistas'
        ordering            = ['user__first_name']

    def __str__(self):
        return f'{self.user.get_full_name() or self.user.username} — {self.get_cargo_display()}'

    # ── Métricas calculadas (usadas no painel de perfil) ──────
    @property
    def total_leads(self):
        return self.user.leads.count()

    @property
    def leads_fechados(self):
        return self.user.leads.filter(status='fechado').count()

    @property
    def taxa_conversao(self):
        if self.total_leads > 0:
            return round((self.leads_fechados / self.total_leads) * 100, 1)
        return 0

    @property
    def receita_total(self):
        from django.db.models import Sum
        total = Financeiro.objects.filter(
            operacao__lead__analista_responsavel=self.user
        ).aggregate(total=Sum('receita'))['total']
        return total or 0

    @property
    def margem_total(self):
        from django.db.models import Sum, F
        result = Financeiro.objects.filter(
            operacao__lead__analista_responsavel=self.user
        ).aggregate(margem=Sum(F('receita') - F('despesa')))['margem']
        return result or 0


# Cria o PerfilAnalista automaticamente quando um User é criado
@receiver(post_save, sender=User)
def criar_perfil_analista(sender, instance, created, **kwargs):
    if created:
        PerfilAnalista.objects.create(user=instance)

@receiver(post_save, sender=User)
def salvar_perfil_analista(sender, instance, **kwargs):
    if hasattr(instance, 'perfil'):
        instance.perfil.save()


# ================================================================
#  EQUIPAMENTO — Catálogo da frota SARENS
# ================================================================

class Equipamento(models.Model):

    class Categoria(models.TextChoices):
        GUINDASTES    = 'guindastes',    'Guindastes'
        MUNCK         = 'munck',         'Caminhões Munck'
        EMPILHADEIRA  = 'empilhadeira',  'Empilhadeiras'
        LINHA_AMARELA = 'linha-amarela', 'Linha Amarela'

    nome       = models.CharField(max_length=100, verbose_name='Nome do equipamento')
    categoria  = models.CharField(max_length=30, choices=Categoria.choices, verbose_name='Categoria')
    capacidade = models.CharField(max_length=60, blank=True, verbose_name='Especificação técnica')
    ativo      = models.BooleanField(default=True, verbose_name='Ativo na frota')

    class Meta:
        verbose_name        = 'Equipamento'
        verbose_name_plural = 'Equipamentos'
        ordering            = ['categoria', 'nome']

    def __str__(self):
        return f'{self.nome} ({self.get_categoria_display()})'


# ================================================================
#  LEAD — Vem do formulário do site
# ================================================================

class Lead(models.Model):

    class Categoria(models.TextChoices):
        GUINDASTES    = 'guindastes',    'Guindastes'
        MUNCK         = 'munck',         'Caminhões Munck'
        EMPILHADEIRA  = 'empilhadeira',  'Empilhadeiras'
        LINHA_AMARELA = 'linha-amarela', 'Linha Amarela'
        OUTRO         = 'outro',         'Outro / Orçamento Personalizado'

    class Subcategoria(models.TextChoices):
        # Guindastes
        AT_100   = 'at-100',   'Guindaste AT 100t'
        RT_200   = 'rt-200',   'Guindaste RT 200t'
        TRE_500  = 'tre-500',  'Guindaste Treliçado 500t'
        # Munck
        MUNCK_10 = 'munck-10', 'Caminhão Munck 10t'
        MUNCK_20 = 'munck-20', 'Caminhão Munck 20t'
        # Empilhadeira
        EMPILH_8 = 'empilh-8', 'Empilhadeira 8t'
        # Linha Amarela
        ESCAV_30 = 'escav-30', 'Escavadeira Hidráulica 30t'
        PA_CARG  = 'pa-carg',  'Pá Carregadeira'
        # Genérico
        OUTRO    = 'outro',    'Outro / A definir'

    class Status(models.TextChoices):
        NOVO           = 'novo',           'Novo'
        EM_ATENDIMENTO = 'em_atendimento', 'Em atendimento'
        FECHADO        = 'fechado',        'Fechado'
        PERDIDO        = 'perdido',        'Perdido'

    nome                 = models.CharField(max_length=200, verbose_name='Nome / Empresa')
    email                = models.EmailField(verbose_name='E-mail')
    telefone             = models.CharField(max_length=20, verbose_name='Telefone / WhatsApp')
    categoria            = models.CharField(max_length=30, choices=Categoria.choices, default=Categoria.OUTRO, verbose_name='Categoria')
    subcategoria         = models.CharField(max_length=30, choices=Subcategoria.choices, default=Subcategoria.OUTRO, blank=True, verbose_name='Subcategoria')
    mensagem             = models.TextField(verbose_name='Descrição da necessidade')
    status               = models.CharField(max_length=20, choices=Status.choices, default=Status.NOVO, verbose_name='Status')
    analista_responsavel = models.ForeignKey(
                             User,
                             on_delete=models.SET_NULL,
                             null=True, blank=True,
                             related_name='leads',
                             verbose_name='Analista responsável'
                           )
    criado_em     = models.DateTimeField(auto_now_add=True, verbose_name='Recebido em')
    atualizado_em = models.DateTimeField(auto_now=True,     verbose_name='Atualizado em')

    class Meta:
        verbose_name        = 'Lead'
        verbose_name_plural = 'Leads'
        ordering            = ['-criado_em']

    def __str__(self):
        return f'{self.nome} — {self.get_categoria_display()} [{self.get_status_display()}]'


# ================================================================
#  OPERAÇÃO — Preenchida pelo analista ao fechar um lead
# ================================================================

class Operacao(models.Model):

    class Turno(models.TextChoices):
        DIURNO   = 'diurno',  'Diurno'
        NOTURNO  = 'noturno', 'Noturno'
        INTEGRAL = '24h',     '24h (Dia e Noite)'

    lead           = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='operacoes', verbose_name='Lead de origem')
    equipamento    = models.ForeignKey(Equipamento, on_delete=models.PROTECT, related_name='operacoes', verbose_name='Equipamento')
    data_inicio    = models.DateField(verbose_name='Data de início')
    data_fim       = models.DateField(verbose_name='Data de término')
    turno          = models.CharField(max_length=10, choices=Turno.choices, default=Turno.DIURNO, verbose_name='Turno')
    local_operacao = models.CharField(max_length=300, blank=True, verbose_name='Local da operação')
    observacoes    = models.TextField(blank=True, verbose_name='Observações técnicas')
    criado_em      = models.DateTimeField(auto_now_add=True, verbose_name='Registrado em')

    class Meta:
        verbose_name        = 'Operação'
        verbose_name_plural = 'Operações'
        ordering            = ['-data_inicio']

    def __str__(self):
        return (
            f'{self.equipamento.nome} | '
            f'{self.data_inicio.strftime("%d/%m/%Y")} → {self.data_fim.strftime("%d/%m/%Y")} '
            f'[{self.get_turno_display()}]'
        )

    def clean(self):
        if self.data_inicio and self.data_fim:
            if self.data_fim < self.data_inicio:
                raise ValidationError({
                    'data_fim': 'A data de término não pode ser anterior à data de início.'
                })

    @property
    def duracao_dias(self):
        if self.data_inicio and self.data_fim:
            return (self.data_fim - self.data_inicio).days + 1
        return 0


# ================================================================
#  FINANCEIRO — Vinculado 1:1 com uma Operação
# ================================================================

class Financeiro(models.Model):

    class StatusPagamento(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        PARCIAL  = 'parcial',  'Parcial'
        PAGO     = 'pago',     'Pago'

    operacao    = models.OneToOneField(Operacao, on_delete=models.CASCADE, related_name='financeiro', verbose_name='Operação')
    receita     = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Receita (R$)', help_text='Valor total cobrado ao cliente')
    despesa     = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Despesa (R$)', help_text='Custo operacional total')
    status_pgto = models.CharField(max_length=10, choices=StatusPagamento.choices, default=StatusPagamento.PENDENTE, verbose_name='Status do pagamento')
    data_pgto   = models.DateField(null=True, blank=True, verbose_name='Data do pagamento')
    observacoes = models.TextField(blank=True, verbose_name='Observações financeiras')

    class Meta:
        verbose_name        = 'Financeiro'
        verbose_name_plural = 'Financeiro'

    def __str__(self):
        return f'Financeiro — {self.operacao} | Margem: R$ {self.margem:.2f}'

    @property
    def margem(self):
        return self.receita - self.despesa

    @property
    def margem_percentual(self):
        if self.receita and self.receita > 0:
            return round((self.margem / self.receita) * 100, 1)
        return 0