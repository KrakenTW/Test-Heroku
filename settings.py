import os

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
instance = os.getenv("INSTANCE")

if instance != 'prod':
    try:
        with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
            SECRET_KEY = f.read().strip()
    except FileNotFoundError:
        SECRET_KEY = "GitHubSecretsDoesntWork"
else:
    SECRET_KEY = os.getenv('SECRET_KEY')
if instance == "prod":
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "projektpb.herokuapp.com","projektpb-mtest-br-mfront.herokuapp.com"]


LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "services",
    "accounts",
    "providers",
    "reservation",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if instance == "prod":
    MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")
ROOT_URLCONF = "urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            (BASE_DIR + "/templates/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
# Heroku config
if 'DATABASE_URL' in os.environ:
    import dj_database_url

    DATABASES = {'default': dj_database_url.config()}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_DIRS = (os.path.join(BASE_DIR, "media", "static"),)
STATIC_URL = "/media/static/"
MEDIA_URL = "media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = BASE_DIR
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
#
# from django.core.mail import EmailMessage
#
# email = EmailMessage(
#     subject = 'Temat',
#     body = 'Treść',
#     from_email = 'uslugrezerwacja@gmail.com',
#     to = ['dawidpawlowski16@gmail.com'],
#     reply_to = ['uslugrezerwacja@gmail.com'],
# )
