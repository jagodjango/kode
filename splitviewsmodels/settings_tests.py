from django.conf import settings

settings.configure(
        INSTALLED_APPS=['splitviewsmodels.apps.SplitviewsmodelsConfig',],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            },
        },
        ROOT_URLCONF='splitviewsmodels.urls_tests',
        )
