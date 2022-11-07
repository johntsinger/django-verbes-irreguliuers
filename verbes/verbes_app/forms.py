from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from verbes_app.models import Table, Verbe, UserProfile


class TableForm(forms.ModelForm):
    class Media:
        extend = False
        css = {
            'all': ('admin/css/base.css', 'admin/css/forms.css',
                    'verbes_app/css/custom_forms.css',
                    'verbes_app/css/widgets_modified.css')
        }

        js = (
            'admin/js/core.js',
            'verbes_app/js/SelectBoxModified.js',
            'verbes_app/js/SelectFilter2Modified.js'
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


class ResetAllForm(forms.Form):
    template_name = 'verbes_app/reset_all_form.html'


class ResetListForm(forms.Form):
    template_name = 'verbes_app/reset_list_form.html'

    def __init__(self, *args, **kwargs):
        # Retrives the 'user' and 'table_id' arguments passed during the instantiation
        # of the class and creates class attributes that will be reused in get_context method
        self.user = kwargs.pop('user', None)
        self.table_id = kwargs.pop('table_id', None)
        super(ResetListForm, self).__init__(self, *args, **kwargs)

    def get_context(self, **kwargs):
        # Creates context
        context = super(ResetListForm, self).get_context(**kwargs)
        user_profile = UserProfile.objects.get(user=self.user)
        table = user_profile.tables.get(id=self.table_id)
        context['table'] = table
        return context


class DeleteListForm(forms.Form):
    template_name = 'verbes_app/delete_list_form.html'

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.table_id = kwargs.pop('table_id', None)
        super(DeleteListForm, self).__init__(self, *args, **kwargs)

    def get_context(self, **kwargs):
        context = super(DeleteListForm, self).get_context(**kwargs)
        if self.user:
            user_profile = UserProfile.objects.get(user=self.user)
            table = user_profile.tables.get(id=self.table_id)
            context['table'] = table
        return context
