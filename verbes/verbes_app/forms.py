from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from verbes_app.models import Table


class TableForm(forms.ModelForm):
    class Media:
        css = {
            'all': ('admin/css/widgets.css', 'admin/css/base.css',
                    'admin/css/forms.css', 'verbes_app/css/custom_forms.css')
        }

    class Meta:
        model = Table
        fields = '__all__'
        widgets = {
            'verbes': FilteredSelectMultiple('verbes', is_stacked=False)
        }