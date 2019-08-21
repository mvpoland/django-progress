SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'djprogress',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}
