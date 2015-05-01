# Django settings for orchestra project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Enable persistent connections
CONN_MAX_AGE = 60*10

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

MEDIA_URL = '/media/'

ALLOWED_HOSTS = '*'


# Set this to True to wrap each HTTP request in a transaction on this database.
# ATOMIC REQUESTS do not wrap middlewares (orchestra.contrib.orchestration.middlewares.OperationsMiddleware)
ATOMIC_REQUESTS = False


MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'orchestra.core.caches.RequestCacheMiddleware',
    # also handles transations, ATOMIC_REQUESTS does not wrap middlewares
    'orchestra.contrib.orchestration.middlewares.OperationsMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS =(
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "orchestra.core.context_processors.site",
)


INSTALLED_APPS = (
    # django-orchestra apps
    'orchestra',
    'orchestra.contrib.accounts',
    'orchestra.contrib.contacts',
    'orchestra.contrib.orchestration',
    'orchestra.contrib.domains',
    'orchestra.contrib.systemusers',
    'orchestra.contrib.mailboxes',
    'orchestra.contrib.lists',
    'orchestra.contrib.webapps',
    'orchestra.contrib.websites',
    'orchestra.contrib.databases',
    'orchestra.contrib.vps',
    'orchestra.contrib.saas',
    'orchestra.contrib.issues',
    'orchestra.contrib.services',
    'orchestra.contrib.plans',
    'orchestra.contrib.orders',
    'orchestra.contrib.miscellaneous',
    'orchestra.contrib.bills',
    'orchestra.contrib.payments',
    'orchestra.contrib.tasks',
    
    # Third-party apps
    'django_extensions',
    'djcelery',
    'djcelery_email',
    'fluent_dashboard',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'rest_framework',
    'rest_framework.authtoken',
    'passlib.ext.django',
    'django_countries',
#    'django_mailer',
    
    # Django.contrib
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin.apps.SimpleAdminConfig',
    
    # Last to load
    'orchestra.contrib.resources',
    'orchestra.contrib.settings',

)


AUTH_USER_MODEL = 'accounts.Account'


AUTHENTICATION_BACKENDS = [
    'orchestra.permissions.auth.OrchestraPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Email config
EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'


#################################
## 3RD PARTY APPS CONIGURATION ##
#################################

# Admin Tools
ADMIN_TOOLS_MENU = 'orchestra.admin.menu.OrchestraMenu'

# Fluent dashboard
# TODO subclass like in admin_tools_menu
ADMIN_TOOLS_INDEX_DASHBOARD = 'orchestra.admin.dashboard.OrchestraIndexDashboard'
FLUENT_DASHBOARD_ICON_THEME = '../orchestra/icons'

FLUENT_DASHBOARD_APP_GROUPS = (
    # Services group is generated by orchestra.admin.dashboard
    ('Accounts', {
        'models': (
            'orchestra.contrib.accounts.models.Account',
            'orchestra.contrib.contacts.models.Contact',
            'orchestra.contrib.orders.models.Order',
            'orchestra.contrib.plans.models.ContractedPlan',
            'orchestra.contrib.bills.models.Bill',
#            'orchestra.contrib.payments.models.PaymentSource',
            'orchestra.contrib.payments.models.Transaction',
#            'orchestra.contrib.payments.models.TransactionProcess',
            'orchestra.contrib.issues.models.Ticket',
        ),
        'collapsible': True,
    }),
    ('Administration', {
        'models': (
            'djcelery.models.TaskState',
            'orchestra.contrib.orchestration.models.Route',
            'orchestra.contrib.orchestration.models.BackendLog',
            'orchestra.contrib.orchestration.models.Server',
            'orchestra.contrib.resources.models.Resource',
            'orchestra.contrib.resources.models.ResourceData',
            'orchestra.contrib.services.models.Service',
            'orchestra.contrib.plans.models.Plan',
            'orchestra.contrib.miscellaneous.models.MiscService',
        ),
        'collapsible': True,
    }),
)

FLUENT_DASHBOARD_APP_ICONS = {
    # Services
    'webs/web': 'web.png',
    'mail/address': 'X-office-address-book.png',
    'mailboxes/mailbox': 'email.png',
    'mailboxes/address': 'X-office-address-book.png',
    'lists/list': 'email-alter.png',
    'domains/domain': 'domain.png',
    'multitenance/tenant': 'apps.png',
    'webapps/webapp': 'Applications-other.png',
    'websites/website': 'Applications-internet.png',
    'databases/database': 'database.png',
    'databases/databaseuser': 'postgresql.png',
    'vps/vps': 'TuxBox.png',
    'miscellaneous/miscellaneous': 'applications-other.png',
    'saas/saas': 'saas.png',
    'systemusers/systemuser': 'roleplaying.png',
    # Accounts
    'accounts/account': 'Face-monkey.png',
    'contacts/contact': 'contact_book.png',
    'orders/order': 'basket.png',
    'plans/contractedplan': 'ContractedPack.png',
    'services/service': 'price.png',
    'bills/bill': 'invoice.png',
    'payments/paymentsource': 'card_in_use.png',
    'payments/transaction': 'transaction.png',
    'payments/transactionprocess': 'transactionprocess.png',
    'issues/ticket': 'Ticket_star.png',
    'miscellaneous/miscservice': 'Misc-Misc-Box-icon.png',
    # Administration
    'settings/setting': 'preferences.png',
    'djcelery/taskstate': 'taskstate.png',
    'orchestration/server': 'vps.png',
    'orchestration/route': 'hal.png',
    'orchestration/backendlog': 'scriptlog.png',
    'resources/resource': "gauge.png",
    'resources/resourcedata': "monitor.png",
    'plans/plan': 'Pack.png',
}

# Django-celery
import djcelery
djcelery.setup_loader()
# Broker
BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_SEND_EVENTS = True
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_DISABLE_RATE_LIMITS = True
# Do not fill the logs with crap
CELERY_REDIRECT_STDOUTS_LEVEL = 'DEBUG'


# rest_framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'orchestra.permissions.api.OrchestraPermissionBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        ('rest_framework.filters.DjangoFilterBackend',)
    ),
}


# Use a UNIX compatible hash
PASSLIB_CONFIG = (
    "[passlib]\n"
    "schemes = sha512_crypt, django_pbkdf2_sha256, django_pbkdf2_sha1,"
    "        django_bcrypt, django_bcrypt_sha256, django_salted_sha1, des_crypt,"
    "        django_salted_md5, django_des_crypt, hex_md5, bcrypt, phpass\n"
    "default = sha512_crypt\n"
    "deprecated = django_pbkdf2_sha1, django_salted_sha1, django_salted_md5,"
    "        django_des_crypt, des_crypt, hex_md5\n"
    "all__vary_rounds = 0.05\n"
    "django_pbkdf2_sha256__min_rounds = 10000\n"
    "sha512_crypt__min_rounds = 80000\n"
    "staff__django_pbkdf2_sha256__default_rounds = 12500\n"
    "staff__sha512_crypt__default_rounds = 100000\n"
    "superuser__django_pbkdf2_sha256__default_rounds = 15000\n"
    "superuser__sha512_crypt__default_rounds = 120000\n"
)
