from django.db import models
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


class Verbe(models.Model):
    present = models.fields.CharField(max_length=50, blank=True)
    preterit = models.fields.CharField(max_length=50, blank=True)
    participe_passe = models.fields.CharField(max_length=50, blank=True)
    francais = models.fields.CharField(max_length=50)

    def __str__(self):
        return f'{self.present} {self.preterit} {self.participe_passe}' + \
               f'{self.francais}'


class Table(models.Model):
    name = models.fields.CharField(max_length=30)
    verbes = models.ManyToManyField(Verbe)
    default = models.fields.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    tables = models.ManyToManyField(Table)
    verbes = models.ManyToManyField(Verbe, related_name='verbes',
        through='UserVerbe')

    def __str__(self):
        return f'{self.user.username if self.user.username else self.user.email}'


class UserTable(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    verbe = models.ForeignKey(Verbe, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE,
        related_name='user_table')
    done = models.fields.BooleanField(default=False)
    success = models.fields.BooleanField(default=False)

    def __str__(self):
        return f'{self.verbe}'


class UserVerbe(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    verbe = models.ForeignKey(Verbe, on_delete=models.CASCADE,
        related_name='user_verbes')
    done = models.fields.BooleanField(default=False)
    success = models.fields.BooleanField(default=False)

    def __str__(self):
        return f'{self.verbe}'


@receiver(m2m_changed, sender=UserProfile.tables.through, dispatch_uid="user_profile_changed")
def user_profile_changed(sender, instance, action, pk_set, **kwargs):
    """Create or delete UserTable if Table objects are added or
    removed from UserProfile.tables m2m"""
    if action == 'post_add':
        # instance is UserProfile object
        for table in instance.tables.filter(id__in=pk_set):
            for verbe in table.verbes.all():
                UserTable.objects.get_or_create(user_profile=instance,
                    table=table, verbe=verbe)
    if action == 'pre_remove':
        instance.usertable_set.filter(user_profile=instance,
            table__id__in=pk_set).delete()
        #for table in instance.tables.filter(id__in=pk_set):
        #UserTable.objects.filter(user_profile=instance,
        #    table__id__in=pk_set).delete()

@receiver(m2m_changed, sender=Table.verbes.through, dispatch_uid="table_changed")
def table_changed(sender, instance, action, pk_set, **kwargs):
    """Create or delete UserTable if Verbe object are added or removed from Table.verbes m2m"""
    if action == 'post_add':
        # instance is Table object
        for verbe in instance.verbes.filter(id__in=pk_set):
            for userprofile in instance.userprofile_set.all():
                UserTable.objects.get_or_create(user_profile=userprofile,
                    table=instance, verbe=verbe)
    if action == 'pre_remove':
        for verbe in instance.verbes.filter(id__in=pk_set):
            for userprofile in instance.userprofile_set.all():
                UserTable.objects.filter(user_profile=userprofile,
                    table=instance, verbe=verbe).delete()
