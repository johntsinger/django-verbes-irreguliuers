from django.contrib import admin
from django import forms
from verbes_app.models import Verbe, Table, VerbeList
from django.contrib.admin.widgets import FilteredSelectMultiple


class VerbeAdmin(admin.ModelAdmin):
    list_display = ('francais', 'present', 'preterit', 'participe_passe',
                    'done', 'success')


class VerbeListInline(admin.TabularInline):
    model = VerbeList


class TableAdminForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['name', 'verbes', 'default']

    verbes = forms.ModelMultipleChoiceField(
        queryset=Verbe.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Verbes',
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(TableAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['verbes'].initial = self.instance.table_verbes.all()

    def save(self, commit=True):
        verbe_list = super(TableAdminForm, self).save(commit=False)
        if commit:
            verbe_list.save()

        if verbe_list.pk:
            verbe_list.verbe_set = self.cleaned_data['verbes']
            self.save_m2m()

        return verbe_list


class TableAdmin(admin.ModelAdmin):
    form = TableAdminForm


admin.site.register(Verbe, VerbeAdmin)
admin.site.register(Table, TableAdmin)
