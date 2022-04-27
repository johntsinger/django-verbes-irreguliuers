from django.contrib import admin
from verbes_app.models import Verbe


class VerbeAdmin(admin.ModelAdmin):
    list_display = ('francais', 'present', 'preterit', 'participe_passe')

admin.site.register(Verbe, VerbeAdmin)