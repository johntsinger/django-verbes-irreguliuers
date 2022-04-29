from django import forms
from verbes_app.models import Table


class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = '__all__'
        widgets = {
            'verbes': forms.SelectMultiple(attrs={'size':'30'})
        }