from django.conf import settings

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# untuk melengkapi test butuh halaman login.html sehingga diputuskan untuk meminjam dari django.contrib.admin
# untuk menggunakan module django.contrib.admin perlu menambahkan sejumlah settings berikut
# 'django.contrib.admin', 'django.contrib.messages', 'django.contrib.messages.middleware.MessageMiddleware'

settings.configure(
    INSTALLED_APPS=['profilpenggunafoto.apps.ProfilpenggunafotoConfig', 'django.contrib.admin', 'django.contrib.auth',
                    'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', ],
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3',
        },
    },
    MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    ROOT_URLCONF='profilpenggunafoto.urls_tests',
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
    MEDIA_URL='/media/',
    MEDIA_ROOT=os.path.join(BASE_DIR, 'media'),
)
