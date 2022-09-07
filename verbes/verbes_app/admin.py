from django.contrib import admin
from django import forms
from verbes_app.models import Verbe, Table, UserTable, UserProfile, UserVerbe
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.urls import resolve
from django.utils.html import format_html
from django.urls import reverse
from django.forms import BaseInlineFormSet


class VerbeAdmin(admin.ModelAdmin):
    list_display = ('francais', 'present', 'preterit', 'participe_passe')


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
            self.fields['verbes'].initial = self.instance.verbes.all()

    def save(self, commit=True):
        verbe = super(TableAdminForm, self).save(commit=False)
        if commit:
            verbe.save()

        if verbe.pk:
            verbe.verbe_set = self.cleaned_data['verbes']
            self.save_m2m()

        return verbe


class TableAdmin(admin.ModelAdmin):
    form = TableAdminForm


class UserVerbeInline(admin.TabularInline):
    model = UserVerbe
    extra = 0
    fields = ('user_verbe', 'done', 'success')
    readonly_fields = ('user_verbe', 'done', 'success')
    classes = ['collapse']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def user_verbe(self, instance):
        """Return a link to UserVerbe change form"""
        app_label = instance._meta.app_label
        model_name = instance._meta.model_name
        admin_url = reverse(f"admin:{app_label}_{model_name}_change",
            args=(instance.pk,))
        return format_html(f"""<a href='{admin_url}'
            target='popup' onclick="window.open('{admin_url}',
            'popup','width=600,height=600');
            return false;">{instance.verbe}</a>""")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user_profile').prefetch_related('user_profile__verbes')


class UserTableInline(admin.TabularInline):
    model = UserTable
    extra = 0
    fields = ('user_table', 'table', 'done', 'success')
    readonly_fields = ('user_table', 'table', 'done', 'success')
    classes = ['collapse']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def user_table(self, instance):
        """Return a link to UserTable change form"""
        app_label = instance._meta.app_label
        model_name = instance._meta.model_name
        admin_url = reverse(f"admin:{app_label}_{model_name}_change",
            args=(instance.pk,))
        return format_html(f"""<a href='{admin_url}' 
            target='popup' onclick="window.open('{admin_url}',
            'popup','width=600,height=600');
            return false;">{instance.verbe}</a>""")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user_profile').prefetch_related('user_profile__tables',
            'user_profile__tables__verbes')


class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

    verbes = forms.ModelMultipleChoiceField(
        queryset=Verbe.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Verbes',
            is_stacked=False
        )
    )

    tables = forms.ModelMultipleChoiceField(
        queryset=Table.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name='Tables',
            is_stacked=False
        )
    )

    def __init__(self, *args, **kwargs):
        super(UserProfileAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['verbes'].initial = self.instance.verbes.all()
            self.fields['tables'].initial = self.instance.tables.all()

    def save(self, commit=True):
        user_profile = super(UserProfileAdminForm, self).save(commit=False)
        if commit:
            user_profile.save()

        if user_profile.pk:
            user_profile.verbes_set = self.cleaned_data['verbes']
            user_profile.tables_set = self.cleaned_data['tables']
            self.save_m2m()

        return user_profile


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm
    inlines = (UserVerbeInline, UserTableInline)


class UserTableAdmin(admin.ModelAdmin):
    list_display = list_display = ('user_profile', 'verbe', 'table', 'done', 'success')


class UserVerbeAdmin(admin.ModelAdmin):
    list_display = list_display = ('user_profile', 'verbe', 'done', 'success')


admin.site.register(Verbe, VerbeAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(UserVerbe, UserVerbeAdmin)
admin.site.register(UserTable, UserTableAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
