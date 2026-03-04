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
STATICFILES_DIRS = [BASE_DIR / 'static']   # ← pasta para o CSS customizado

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

    # Carrega o CSS customizado
    "STYLES": [
        lambda request: static("css/sarens_admin.css"),
    ],

    # Dourado SARENS calibrado (#C8A84B)
    "COLORS": {
        "primary": {
            "50":  "253 248 235",
            "100": "249 237 196",
            "200": "243 220 143",
            "300": "235 198 90",
            "400": "218 179 65",
            "500": "200 168 75",   # #C8A84B — dourado principal
            "600": "170 138 50",
            "700": "135 105 35",
            "800": "95  72  20",
            "900": "60  44  10",
            "950": "35  25   5",
        },
        "base": {
            "50":  "250 250 250",
            "100": "240 240 240",
            "200": "220 220 220",
            "300": "180 180 180",
            "400": "130 130 130",
            "500": "90  90  90",
            "600": "60  60  60",
            "700": "40  40  40",
            "800": "28  28  28",   # --sarens-dark-2
            "900": "20  20  20",   # --sarens-dark
            "950": "13  13  13",   # --sarens-black
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