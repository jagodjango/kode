from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from profilpenggunafoto.models import Profil


# https://docs.djangoproject.com/en/dev/topics/auth/customizing/#extending-the-existing-user-model
# Define an inline admin descriptor for Profil model
# which acts a bit like a singleton
class ProfilInline(admin.StackedInline):
    model = Profil
    can_delete = False
    verbose_name_plural = 'profiles'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfilInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
