from django.conf import settings

settings.configure(
        INSTALLED_APPS=['halo.apps.HaloConfig',],
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite',
            },
        },
        ROOT_URLCONF='halo.tests_urls',
        )
