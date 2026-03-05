from pathlib import Path
from django.templatetags.static import static

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-+49tggs97wvyc8y74_5q5i70d834v#0b^lcdvx81yjv9wmw_k*'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'contatos',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE     = 'America/Sao_Paulo'
USE_I18N      = True
USE_TZ        = True

STATIC_URL  = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

EMAIL_BACKEND       = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = 'maxpesa.tecnologia@gmail.com'
EMAIL_HOST_PASSWORD = 'kazv ulkb kuzx ulpt'
DEFAULT_FROM_EMAIL  = EMAIL_HOST_USER

CORS_ALLOW_ALL_ORIGINS = True

# ================================================================
#  UNFOLD — Tema SARENS
# ================================================================
UNFOLD = {
    "SITE_TITLE":  "SARENS",
    "SITE_HEADER": "SARENS — Painel Operacional",
    "SITE_URL":    "/",
    "SITE_SYMBOL": "settings",
    "THEME": "light",

    "STYLES": [
        lambda request: static("css/sarens_admin.css"),
    ],

    "COLORS": {
        # Primário = dourado SARENS — botões, links, destaques
        "primary": {
            "50":  "253 248 225",
            "100": "250 240 190",
            "200": "245 225 145",
            "300": "235 205 95",
            "400": "220 183 65",
            "500": "200 168 75",
            "600": "168 138 52",
            "700": "130 104 35",
            "800": "90  70  20",
            "900": "55  42  10",
            "950": "30  22   4",
        },
        # Base = escala de cinza quente — sidebar, texto, fundos
        # No light mode: 50=fundo sidebar, 100=hover, 900=texto
        "base": {
            "50":  "250 248 244",
            "100": "243 240 233",
            "200": "225 220 210",
            "300": "190 184 172",
            "400": "148 142 130",
            "500": "105 100 88",
            "600": "70  66  56",
            "700": "48  45  37",
            "800": "30  28  22",
            "900": "18  17  13",
            "950": "10   9   6",
        },
    },

    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Visão Geral",
                "separator": False,
                "items": [
                    {"title": "Dashboard", "icon": "dashboard", "link": "/admin/dashboard/"},
                ],
            },
            {
                "title": "Comercial",
                "separator": True,
                "items": [
                    {"title": "Leads",      "icon": "inbox",        "link": "/admin/contatos/lead/"},
                    {"title": "Operações",  "icon": "engineering",  "link": "/admin/contatos/operacao/"},
                    {"title": "Financeiro", "icon": "payments",     "link": "/admin/contatos/financeiro/"},
                ],
            },
            {
                "title": "Frota",
                "separator": True,
                "items": [
                    {"title": "Equipamentos", "icon": "construction", "link": "/admin/contatos/equipamento/"},
                ],
            },
            {
                "title": "Equipe",
                "separator": True,
                "items": [
                    {"title": "Analistas", "icon": "group",          "link": "/admin/contatos/perfilanalista/"},
                    {"title": "Usuários",  "icon": "manage_accounts","link": "/admin/auth/user/"},
                ],
            },
        ],
    },
}