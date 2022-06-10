from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from verbes_app.models import Table, Verbe


class TableForm(forms.ModelForm):
    class Media:
        extend = False
        css = {
            'all': ('admin/css/base.css', 'admin/css/forms.css',
                    'verbes_app/css/custom_forms.css',
                    'verbes_app/css/widgets_modified.css')
        }

        js = (
            "admin/js/core.js",
            "verbes_app/js/SelectBoxModified.js",
            "verbes_app/js/SelectFilter2Modified.js"
        )

    class Meta:
        model = Table
        exclude = ('default',)
        labels = {
            'name': 'Nom de la liste',
        }
        widgets = {
            'verbes': FilteredSelectMultiple('verbes', is_stacked=False)
        }


class VerbeForm(forms.ModelForm):
    class Meta:
        model = Verbe
        exclude = ('francais', 'done', 'success')
