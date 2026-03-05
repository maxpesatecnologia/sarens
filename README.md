# SARENS — Sistema de Gestão Operacional

Painel interno para gestão de leads, operações e frota da SARENS. Desenvolvido com Django + Unfold Admin.

---

## Requisitos

- Python 3.11+
- pip
- Git

---

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/sarens.git
cd sarens
```

### 2. Criar e ativar o ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
cd backend_sarens
pip install -r requirements.txt
```

### 4. Aplicar as migrações

```bash
python manage.py migrate
```

### 5. Iniciar o servidor

```bash
python manage.py runserver
```

Acesse o painel em: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

> **Acesso ao painel:** usuários e permissões são gerenciados pelo administrador do sistema em **Equipe → Usuários**. Novos colaboradores devem solicitar acesso ao responsável.

---

## Estrutura do Projeto

```
sarens/
├── .venv/                     # Ambiente virtual (não versionar)
├── backend_sarens/
│   ├── contatos/              # App principal
│   │   ├── migrations/
│   │   ├── templates/
│   │   │   └── admin/
│   │   │       └── dashboard.html
│   │   ├── admin.py           # Configuração do painel
│   │   ├── models.py          # Modelos: Lead, Operacao, Financeiro...
│   │   └── views.py           # Views + dashboard
│   ├── core/
│   │   ├── settings.py        # Configurações Django + Unfold
│   │   └── urls.py            # Rotas
│   ├── static/
│   │   └── css/
│   │       └── sarens_admin.css
│   └── manage.py
├── requirements.txt
└── README.md
```

---

## Dependências

| Pacote | Versão | Descrição |
|---|---|---|
| Django | 6.0.2 | Framework principal |
| django-unfold | 0.82.0 | Tema moderno para o Django Admin |
| django-cors-headers | latest | Permite requisições cross-origin do frontend |
| Pillow | latest | Suporte a upload de imagens (foto do analista) |

---

## Configurações sensíveis

As seguintes variáveis no `settings.py` devem ser alteradas antes de ir para produção:

- `SECRET_KEY` — gere uma nova chave em: https://djecrety.ir
- `DEBUG` — alterar para `False`
- `EMAIL_HOST_PASSWORD` — senha de app do Gmail do ambiente de produção
- `ALLOWED_HOSTS` — adicionar o domínio do servidor

---

## Frontend (Site)

O site estático está na raiz do projeto. Para servir localmente:

```bash
cd sarens
python -m http.server 3000
```

---

## Licença

Uso interno — Grupo Maxpesa © 2026
