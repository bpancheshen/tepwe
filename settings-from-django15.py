# Django settings for Plains Cree Oahpa project.
# -*- encoding: utf-8 -*-
import os.path
import sys

os.environ['PYTHON_EGG_CACHE'] = '/tmp'
os.environ['DJANGO_SETTINGS_MODULE'] = 'crk_oahpa.settings'

# WSGI stuff
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# Confirm this is in path.
path = '/srv/apps/oahpa/nehiyawetan/crk_oahpa/'
if path not in sys.path:
    sys.path.append(path)

# This flag triggers now the URL patterns in url.py file.
# The production_setting.py is triggered now by os name.
DEV = False

# Can just list the media or template dirs as here('templates') instead of '/home/me/.../smaoahpa/templates/

here = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), x)
here_cross = lambda x: os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), *x) 

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',
)

# just testing svn
ADMINS = (
#   ('Ciprian Gerstenberger', 'ciprian.gerstenberger@uit.no'),
#   ('Trond Trosterud', 'trond.trosterud@uit.no'),
#   ('Lene Antonsen', 'lene.antonsen@uit.no'),
#   ('Ryan Johnson', 'rjo040@post.uit.no'),
        ('Ryan Johnson', 'ryan.txanson@gmail.com')
)

MANAGERS = ADMINS

# This is overridden below if the hostname is right.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/srv/apps/oahpa/nehiyawetan/crk_oahpa/db.sqlite',
        # 'NAME': 'crk_oahpa',
        # 'USER': 'crk_oahpa',
        # 'PASSWORD': 'Blah',
        # 'HOST': 'localhost',
        # 'PORT': '3052',
        # 'OPTIONS': {
        #      'read_default_file': '/etc/my.cnf',
        #      # 'charset': 'utf8',
        #      'init_command': 'SET storage_engine=INNODB', #  ; SET table_type=INNODB',
        #  }
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.

TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# http://oahpa.no/nehiyawetan/

URL_PREFIX = 'nehiyawetan'

# Absolute path to the directory that holds media.
MEDIA_ROOT = "/srv/apps/oahpa/nehiyawetan/crk_oahpa/media/"
#MEDIA_ROOT = here('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"

MEDIA_URL = '/nehiyawetan/media/'
STATIC_URL = '/nehiyawetan/media/'

# MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/%s/admin/media/' % URL_PREFIX

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+&dhg83#u^mg$vnp^7u2xd8wo15&=_c#yf0*no-mzrej!@zdw_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'courses.authentication.CookieAuthMiddleware',
    # 'courses.middleware.GradingMiddleware',
)

ROOT_URLCONF = 'crk_oahpa.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),
    os.path.join(os.path.dirname(__file__), 'crk_drill/templates').replace('\\','/'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.csrf",
    # "crk_oahpa.courses.context_processors.request_user",
    # "crk_oahpa.courses.context_processors.courses_user",
    # "crk_oahpa.survey.context_processors.display_survey_notice",
    "crk_oahpa.conf.context_processors.dialect",
    "crk_oahpa.conf.context_processors.site_root",
    # "crk_oahpa.conf.context_processors.redirect_to",
    # "crk_oahpa.conf.context_processors.grammarlinks",
    'django_messages.context_processors.inbox',
)
#               "management.context_processors.admin_media_prefix")


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
        #'openid_provider',
    'errorapi',
    'crk_oahpa.crk_drill',
    'crk_oahpa.conf',
    'crk_oahpa.courses',
    'crk_oahpa.crk_feedback',
    'crk_oahpa.management'
)


# We have to disable all the languages we're not using for
# internationalizations, otherwise they end up getting set if django
# detects them in the user's browser
LANGUAGES = (
    ('en', 'English'),
    # ('crk', 'Plains Cree'),
    # ('ru', 'Russian'),    
    # ('sme', 'North Sami'),
    # ('no', 'Norwegian'),
    # ('sv', 'Swedish'),
    # ('fi', 'Finnish'),
    # ('de', 'German'),
)

OLD_NEW_ISO_CODES = {
    "fi": "fin",
    "ru": "rus",
    "en": "eng",
    "no": "nob",
    "de": "deu",
    "sv": "swe",
    "sma": "sma",
        "sme": "sme",
        "crk": "crk"
} 

# Regular expression and language code. Regexp must apply 'inf' group to
# matched string. 

# If infinitive is None, then we assume there is no similar infinitive
# presentation marking, or that it comes from tags for languages which
# have word forms in the system.


INFINITIVE_SUBTRACT = {
    'nob': ur'^(?P<inf>å )?(?P<lemma>.*)$',
    'swe': ur'^(?P<inf>att )?(?P<lemma>.*)$',
    'eng': ur'^(?P<inf>to )?(?P<lemma>.*)$',
    'deu': ur'^(?P<inf>zu )?(?P<lemma>.*)$',
}

INFINITIVE_ADD = {
    'nob': ur'å \g<lemma>',
    'swe': ur'att \g<lemma>',
    'eng': ur'to \g<lemma>',
    'deu': ur'zu \g<lemma>',
}

DIALECTS = {
    'main': ('generator-oahpa-gt-norm.hfstol', 'Unrestricted'),
#   'GG': ('isme-GG.restr.fst', 'Western'),
#   'KJ': ('isme-KJ.restr.fst', 'Eastern'),
    'NG': (None, 'Non-Presented forms'),
}

ENG_FST_DIRECTORY = '../crk/englexc/'
ENG_DIALECTS = {
    'main': ('../crk/englexc/ieng.fst', 'Unrestricted'),
}

ENG_HLOOKUP_TOOL = '/usr/local/bin/lookup'
ENG_LOOKUP_TOOL = '/usr/local/bin/lookup -flags mbTT'

DEFAULT_DIALECT = 'main'
NONGEN_DIALECT = 'NG'
# # # 
#
# Some settings for the install.py scripts
#
# # # 

# maybe some of these actually should be options in the install script... 

MAIN_LANGUAGE = ('crk', 'Plains Cree')
L1 = MAIN_LANGUAGE[0]
LOOKUP_OPTS = ''

# NB: this is a problem-- when installing we need to use HFST for
# everything, but when running oahpa needs to use xfst for numra
# must fix.

# when running ... 
LOOKUP_TOOL = '/usr/bin/lookup' # xfst
HLOOKUP_TOOL = '/usr/bin/hfst-lookup' # hfst

LOOKUP_TOOL = '/usr/bin/lookup' # hfst 
LOOKUP_OPTS = '-flags mbTT'

# when installing ... 
if 'install.py' in sys.argv:
    LOOKUP_TOOL = '/usr/bin/hfst-optimized-lookup'
    LOOKUP_OPTS = '-qx'

    #LOOKUP_TOOL = '/opt/sami/xerox/c-fsm/ix86-linux2.6-gcc3.4/bin/lookup'

FST_DIRECTORY = '/opt/smi/crk/bin'
LOG_FILE = path + '/crk_drill/vastaF_log.txt'

GAME_FSTS = {
    'dato': {
        'generate': FST_DIRECTORY + '/transcriptor-date-digit2text.filtered.lookup.xfst',
        'answers': FST_DIRECTORY + '/transcriptor-date-text2digit.filtered.lookup.xfst',
    },
    'numbers': {
        'generate': FST_DIRECTORY + '/transcriptor-numbers-digit2text.filtered.lookup.xfst',
        'answers': FST_DIRECTORY + '/transcriptor-numbers-text2digit.filtered.lookup.xfst',
    },
    'clock': {
        'generate': FST_DIRECTORY + '/transcriptor-clock-digit2text.filtered.lookup.xfst',
        'answers': FST_DIRECTORY + '/transcriptor-clock-text2digit.filtered.lookup.xfst',
    },
    'money': {
        'generate': FST_DIRECTORY + '/transcriptor-money-digit2text.filtered.lookup.xfst',
        'answers': FST_DIRECTORY + '/transcriptor-money-text2digit.filtered.lookup.xfst',
    },
}


# #
#
# LOGGING
#
# #

# TODO: logging!
# http://docs.djangoproject.com/en/dev/topics/logging/

# from production_settings import *

MEDIA_PREFIX = '/nehiyawetan/media/'


# #
#
# USER PROFILES
#
# #

AUTH_PROFILE_MODULE = 'courses.UserProfile'
LOGIN_REDIRECT_URL = '/%s/courses/' % URL_PREFIX
LOGIN_URL = '/%s/courses/login/' % URL_PREFIX

CACHES = {
        'default': {
                'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                'LOCATION': '/var/tmp/crk_oahpa_cache'
        },
}

_join_path = lambda x: os.path.join(os.getcwd(), x)

ERROR_FST_SETTINGS = {
    'lookup_tool': 'hfst-optimised-lookup',
    'fst_path': '/opt/smi/crk/bin/transcriptor-numbers-text2digit.filtered.lookup.hfstol',
    'error_log_path': '/srv/apps/oahpa/nehiyawetan/crk_oahpa/error_fst_log.txt',
    'error_message_files': {
        'eng': '/srv/apps/oahpa/nehiyawetan/crk/meta/errorfstmessages.xml',
    }
}

USE_X_FORWARDED_HOST = True
