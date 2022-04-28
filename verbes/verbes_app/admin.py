from django.contrib import admin
from verbes_app.models import Verbe, Table


class VerbeAdmin(admin.ModelAdmin):
    list_display = ('francais', 'present', 'preterit', 'participe_passe')


class TableAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Verbe, VerbeAdmin)
admin.site.register(Table, TableAdmin)